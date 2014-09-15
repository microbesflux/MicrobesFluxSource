# Model = FluxModel
import os
from time import gmtime, strftime

from flux.models import Profile
from flux.models import Task
from flux.storage import usl # Unified Storage Library
from flux.task.task import send_mail
from flux.view.foundations import *
from flux.view.json import Json

    ####################################################
    #############  Objective Function   ################
    ####################################################

def _process_object_update(input_params, pathway):
    key      = str(input_params["pk"])
    reaction = str(input_params["r"])
    w        = input_params["w"]
    weight   = float(w)
    pathway.objective[reaction] = weight
    r = Json()
    r.add_pair("pk", key)
    r.add_pair("r",  reaction)
    r.add_pair("w",  str(weight))
    return r

def _process_object_fetch(pathway):
    weights = pathway.get_objective_weights()
    ret = Json("array")
    public_key = 1
    for name in pathway.reactions:
        j = Json()
        j.add_pair("pk", public_key)
        public_key +=1
        j.add_pair("r", name)
        if name not in weights:
            weight[name] = 1.0
        j.add_pair("w", str(weights[name]))
        ret.add_item(j)
    return ret

    ####################################################
    #############  SV =0 constraints    ################
    ####################################################

def _process_sv_fetch(pathway):
    sv = pathway.get_sv()
    ret = Json("array")
    for name in sv:
        j = Json()
        j.add_pair("c", pathway.get_long_name(name))
        j.add_pair("r", ''.join(sv[name]) + " = 0")
        ret.add_item(j)
    return ret


    ####################################################
    #############  Variable bounds      ################
    ####################################################

def _process_boundary_fetch(pathway):
    boundarys = pathway.get_bounds()
    ret = Json("array")
    public_key = 0
    for name in boundarys:
        j = Json()
        j.add_pair("pk", public_key)
        public_key +=1
        j.add_pair("r", name)
        j.add_pair("l", str(boundarys[name][0]))
        j.add_pair("u", str(boundarys[name][1]))
        ret.add_item(j)
    return ret

def _process_boundary_update(input_params, pathway):
    bound = pathway.get_bounds()
    key = str(input_params["pk"])
    reactionid = str(input_params["r"])
    lb = float(input_params["l"].encode('ascii', 'ignore'))
    ub = float(input_params["u"].encode('ascii', 'ignore'))
    bound[reactionid][0] = lb
    bound[reactionid][1] = ub
    j = Json()
    j.add_pair("pk", key)
    j.add_pair("r", reactionid)
    j.add_pair("l", str(lb))
    j.add_pair("u", str(ub))
    return j

################## Functions used by url.py ###############

#@save_required
@ajax_callback
@table_response_envelope
def user_obj_fetch(request):
    """ Get the user-defined objective function weights"""
    pathway = get_pathway_from_request(request)
    # if it is the first time fetch is called. We will init all weight to 1.
    result = _process_object_fetch(pathway)
    # Save the session because fetch might change the underlying pathway
    save_pathway(request, pathway)
    return result

#@save_required
@ajax_callback
@response_envelope
def user_obj_update(request):
    """ Get the objective as BIOMASS """
    pathway = get_pathway_from_request(request)
    result = _process_object_update(request.GET, pathway)
    save_pathway(request, pathway)
    return result

@ajax_callback
@table_response_envelope
def sv_fetch(request):
    """ Get the SV = 0 term"""
    pathway = get_pathway_from_request(request)
    return _process_sv_fetch(pathway)

#@save_required
@ajax_callback
@table_response_envelope
def user_bound_fetch(request):
    """ Get the upper and lower bound"""
    pathway = get_pathway_from_request(request)

    result = _process_boundary_fetch(pathway)
    # Necessary because we do lazy boundary initialization. When the first time boundary
    # fetch is called on a pathway, we init the boundary.
    save_pathway(request, pathway)
    return result

#@save_required
@ajax_callback
@response_envelope
def user_bound_update(request):
    """ Update the upper and lower bound"""
    pathway = get_pathway_from_request(request)
    result = _process_boundary_update(request.GET, pathway)
    save_pathway(request, pathway)
    return result


# TODO: use unified file system to store those intermediate files.
from django.core.files.storage import FileSystemStorage
import subprocess

def write_pathway_for_plot(pathway, n):
    node_adj = {}
    for rname, r in pathway.reactions.iteritems():
        if r.products and r.substrates:
            if r.name not in node_adj:
                node_adj[r.name] = []
            for s in r.substrates:
                for p in r.products:
                    if s not in node_adj:
                        node_adj[s] = []
                    node_adj[s].append(r.name)
                    node_adj[r.name].append(p)
    fs = FileSystemStorage()
    f = fs.open(n + ".adjlist", "w")
    for key, item in node_adj.iteritems():
        f.write(key)
        f.write(' ')
        f.write(' '.join(item))
        f.write('\n')
    f.close()

from django.http import HttpResponse

def svg(request):
    pathway = get_pathway_from_request(request)
    n = request.session['collection_name']
    email = request.session['provided_email']
    write_pathway_for_plot(pathway, n)
    # Add a task to task queue.
    t = Task(task_type = 'svg', main_file = n, email = email, additional_file = '', status = "TODO")
    t.save()
    return HttpResponse(content = "SVG Task submitted", status = 200, content_type = "text/html")

def sbml(request):
    n = request.session['collection_name']
    address = request.session['provided_email']
    pathway = get_pathway_from_request(request)

    fs = FileSystemStorage()
    f = fs.open(n + ".sbml", "w")
    pathway.output_sbml(f, str(n))
    f.close()
    attachments = [ n + ".sbml"]
    send_mail(address, attachments, title="SBML")
    return HttpResponse(content = "SBML file send.", status = 200, content_type = "text/html")

def optimization(request):
    pathway = get_pathway_from_request(request)
    n = request.session['collection_name']
    email = request.session['provided_email']

    obj_type = request.GET['obj_type']
    ot = 'biomass'
    if obj_type == '0':  # customer defined
        ot = 'user'
    fs = FileSystemStorage()
    f = fs.open(n + ".ampl", "w")
    mapf = fs.open( n + ".map", "w")
    reportfile = fs.open(n + "_header.txt", "w")
    pathway.output_ampl(f, mapf, reportfile, objective_type = ot )
    f.close()
    mapf.close()
    reportfile.close()

    t = Task(task_type = 'fba', main_file = n, email = email, additional_file = '', status = "TODO")
    t.save()

    # Locate user data (if any) and update their profiles
    u = request.user
    pro = None

    if not u.is_anonymous():
        try:
            pro = Profile.objects.get(user = u, name = n)
        except Profile.DoesNotExist:
            pass

    if pro:
        pro.status="submitted"
        pro.model_type = "fba"
        import datetime
        pro.submitted_date = str(datetime.datetime.now())
        pro.save()

    return HttpResponse(content = "New Optimization problem submitted .. ", status = 200, content_type = "text/html")


""" Check names against all the user-defined pathway"""
""" This function checks the validity of the user uploaded file"""
def check_user_upload_file_format(pathway, f):
    if not f:
        print "can't read file"
        return False
    header = f.readline().split()
    length = len(header)
    # print "Header is", header
    # print "Header length is", length, " user defined is ", pathway.user_pathway
    if length != len(pathway.user_pathway):
        print "Length mismatch 1"
        return False
    for h in header:
        h = h.strip(' ')
        if not pathway.check_user_pathway(h):
            print "can't find pathway '" + h + "'"
            return False
    for lines in f:
        t = lines.strip(' ')
        t = t.strip('\n')
        if len(t)==0:   # Skip empty line
            continue
        if t[0] == "#":
            continue
        try:            # see if they are all numbers
            numbers = map(float, lines.split())
        except:
            print "Can not convert to float"
            return False
        if len(numbers) != length:  #
            print "Number length is not correct"
            return False
    return True

""" This function checks the validity of the user uploaded file"""
# TO delete
def old_check_user_upload_file_format(f):
    if not f:
        return False
    header = f.readline().split(",")
    if header[0].lower() != "time":
        return False# it has to be time
    if header[1].lower() != "biomass":
        return False
    length = len(header)
    current = -1.0
    for lines in f:
        try:
            numbers = map(float, lines.split(","))
        except:
            return False
        if len(numbers) != length:
            return False
        if numbers[0] <= current:
            return False
        current = numbers[0]
    return True

def file_upload(request):
    """ Upload a file  from client """
    q = request.POST
    f = request.FILES['uploadFormElement']

    pathway = get_pathway_from_request(request)
    newkey = usl.create("dfba")       # Put it in dfba namespace
    destination = usl.get(newkey)
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

    destination = usl.get(newkey)
    if check_user_upload_file_format(pathway, destination):
        destination.close()
        request.session["dfba_upload"] = newkey
        return HttpResponse(content = """Successfully Uploaded. \n File key is """ + newkey, status = 200, content_type = "text/html")
    else:
        destination.close()
        usl.delete(newkey)      # not reserve that file
        return HttpResponse(content = """Please check your file format""", status = 200, content_type = "text/html")

""" Let the user enter flux values """
def dfba_solve(request):
    pathway = get_pathway_from_request(request)
    name = request.session["collection_name"]
    associated_file_key = request.session["dfba_upload"]
    email = request.session['provided_email']

    # Use usl to assign a new key
    fs = FileSystemStorage()
    f = fs.open(name + ".ampl", "w")
    mapf = fs.open( name + ".map", "w")
    reportfile = fs.open(name + "_header.txt", "w")

    additional = fs.open("dfba/" + associated_file_key, "r")

    obj_type = request.GET['obj_type']
    ot = 'biomass'	# 1 = biomass
    if obj_type == '0':  # 0 = customer defined
        ot = 'user'
    pathway.output_ampl(f, mapf, reportfile, model_type="dfba", additional_file = additional, objective_type = ot)
    additional.close()

    f.close()
    mapf.close()
    reportfile.close()
    t = Task(task_type = 'dfba', main_file = name, email = email, additional_file = associated_file_key, status = "TODO")
    t.save()
    return HttpResponse(content = "New DFBA optimization problem submitted .. ", status = 200, content_type = "text/html")

# TODO(xuy): change this to a different file transport mechanism
def test_ssh(request):
    p = subprocess.Popen("/research-www/engineering/tanglab/flux/test_scp_to_cloud.sh ", shell=True)
    sts = os.waitpid(p.pid, 0)[1]
    return HttpResponse(content = "A file should have been copied to cloud by now. ", status = 200, content_type = "text/html")

##############################
###### TRASH  ##############

########## New code to be added
### Later change to borg pattern
class FileManager(object):
    def get_new_file_name(self, suffix):
        return "new" + suffix
    def store(self, name):
        return
    def remove(self, name):
        return

def generate_diff_file(data, target, signature):
    X0 = float(data[0].split()[1])
    flag = 1
    for i in xrange(len(data) - 1):
        target.write(str(flag))
        target.write("\t")
        flag += 1
        up = map(float, data[i].split())
        down = map(float, data[i + 1].split())
        count = 0
        for j, k in zip(up, down):
            if count == 1:   # case for X
                target.write(str(j))
            elif count >= 2:
                target.write(str((k - j) * signature[count - 2]))
            else:
                target.write(str(k - j))    # for the first field, actually
            target.write("\t")
            count += 1
        target.write("\n")
    return X0

def generate_diff_header(header, target, pathway, signature):
    target.write("param:\tstep\t")
    h = header.split()
    target.write(h[0])
    target.write("\t")
    target.write(h[1])
    target.write("\t")
    r = []
    for name in header.split()[2:]:
        s = pathway.external_compond_to_flux(name, signature)
        r.append(s)
        target.write(str(s))
        target.write("\t")
    target.write(":=\n")
    return r
