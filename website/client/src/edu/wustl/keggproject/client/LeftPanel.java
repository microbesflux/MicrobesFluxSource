package edu.wustl.keggproject.client;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Anchor;
import com.google.gwt.user.client.ui.StackPanel;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.user.client.ui.Widget;

// Xueyang
public class LeftPanel {
	private RightPanel rp;
	private StatusFormPanel sf;

	private AccountManagementPanel am;
	
	public void setRightPanel(RightPanel r) {
		rp = r;
	}

	public void setStatusFormPanel(StatusFormPanel sfp) {
		sf = sfp;
	}

	public void setAccountManagementPanel(AccountManagementPanel amp) {
		am = amp;
	}
	
	public Widget getLeftPanel() {

		final VerticalPanel filePanel = new VerticalPanel();
		final Anchor newFile = new Anchor("New model");
		final Anchor loadFile = new Anchor("Load model");
		final Anchor saveFile = new Anchor("Save model");
		final Anchor saveFileAs = new Anchor("Save model As");
		final Configuration conf = ConfigurationFactory.getConfiguration();

		newFile.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				if (conf.getCurrentCollection().length() > 0) {
					boolean proceed = Window
						.confirm("You are about to create a new model. Make sure to save all changes (if any) to your current model. Do you want to proceed? ");
					if (!proceed) {
							return;
					}
				}
				rp.changeToNewFile();
			}
		});

		loadFile.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {

				if (conf.getLogin() == false) {
					Window.alert("You have to login first to load existing models");
					return;
				}
				
				if (conf.getCurrentCollection().length() > 0) {
					boolean proceed = Window
							.confirm("You are about to load a new model. Changes to the current model will be discarded unless you click \"Save Model\" first. Do you want to proceed? ");
					if (!proceed) {
						return;
					}
				}
				
				sf.loadFile();
				rp.changeToWelcome();
			}
		});

		saveFile.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				if (conf.getLogin() == false) {
					Window.alert("You have to login first to save existing models");
					return;
				}
				
				sf.saveFile(false);
			}
		});

		saveFileAs.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				if (conf.getLogin() == false) {
					Window.alert("You have to login first to save existing models");
					return;
				}
				
				// rp.ChangeToPathway();
				sf.saveFileAs();
			}
		});

		filePanel.add(newFile);
		filePanel.add(loadFile);
		filePanel.add(saveFile);
		filePanel.add(saveFileAs);

		VerticalPanel functionPanel = new VerticalPanel();
		final Anchor genomeInfo = new Anchor("Genome Information");
		final Anchor pathwayInfo = new Anchor("Metabolic Pathways");
		final Anchor optimizationInfo = new Anchor("Optimization");
		genomeInfo.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				rp.changeToGenome();
			}
		});
		pathwayInfo.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				rp.ChangeToPathway();
			}
		});
		optimizationInfo.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				rp.ChangeToOptimization();
			}
		});
		functionPanel.add(genomeInfo);
		functionPanel.add(pathwayInfo);
		functionPanel.add(optimizationInfo);

		VerticalPanel accountPanel = new VerticalPanel();
		final Anchor summaryHistory = new Anchor("Summary");
		final Anchor passwordChange = new Anchor("Change Passwords");
		summaryHistory.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				if (conf.getLogin() == false) {
					Window.alert("You have to login first to view your usage summary.");
					return;
				}
				
				am.ChangeToSummary();
			}
		});
		passwordChange.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				if (conf.getLogin() == false) {
					Window.alert("You have to login first to change your password.");
					return;
				}
				
				am.ChangeToPasswordChange();
			}
		});
		
		accountPanel.add(summaryHistory);
		accountPanel.add(passwordChange);

		StackPanel leftPanel = new StackPanel();
		leftPanel.add(filePanel, "Build/Load/Save a Model", false);
		leftPanel.add(functionPanel, "Pathways & FBA", false);
		leftPanel.add(accountPanel, "Account Management", false);

		return leftPanel;
	}
}
