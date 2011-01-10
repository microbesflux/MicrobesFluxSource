package edu.wustl.keggproject.client;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.Grid;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.PasswordTextBox;
import com.google.gwt.user.client.ui.SimplePanel;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.user.client.ui.Widget;
import com.google.gwt.user.client.ui.FormPanel.SubmitCompleteEvent;
import com.google.gwt.user.client.ui.FormPanel.SubmitEvent;
import com.smartgwt.client.widgets.grid.ListGrid;
import com.smartgwt.client.widgets.grid.ListGridField;

import edu.wustl.keggproject.client.datasource.PathwayDS;
import edu.wustl.keggproject.client.datasource.accountSummaryDS;

public class AccountManagementPanel {
 
	public SimplePanel accountManagementPanel = new SimplePanel();
	
	public Widget getAccountManagementPanel(){
		return accountManagementPanel;
	}
	public void initialize() {
		accountManagementPanel.setVisible(false);
	}
	
	public void ChangeToSummary(){
		accountManagementPanel.clear();
		accountManagementPanel.setVisible(true);
		
		VerticalPanel summaryPanel= new VerticalPanel();
		
		final ListGrid accountSummary = new ListGrid();
		accountSummary.setWidth(400);
		accountSummary.setHeight(500);
		accountSummary.setShowAllRecords(true);
		accountSummary.setDataSource(accountSummaryDS.getInstance());

		ListGridField date = new ListGridField("date");
		ListGridField model = new ListGridField("model");
		ListGridField type = new ListGridField("type");
		ListGridField status = new ListGridField("status");
		
		accountSummary.setFields(date, model, type, status);
		accountSummary.setAutoFetchData(true);
		
		Button buttonExit=new Button("Exit Summary");
		buttonExit.addClickHandler(new ClickHandler(){
			public void onClick(ClickEvent event) {
				accountManagementPanel.setVisible(false);
			}
		});
		
		summaryPanel.add(accountSummary);
		summaryPanel.add(buttonExit);
		accountManagementPanel.setWidget(summaryPanel);
	}
	public void ChangeToPasswordChange(){
		accountManagementPanel.clear();
		accountManagementPanel.setVisible(true);
		
		final FormPanel changePassword = new FormPanel();
		Grid changePasswordGrid = new Grid(4,2);
		Label oldPassword = new Label("Old Password");
		final PasswordTextBox oldPasswordBox = new PasswordTextBox();
		Label newPassword = new Label("New Password");
		final PasswordTextBox newPasswordBox = new PasswordTextBox();
		Label confirmPassword = new Label("Confirm Password");
		final PasswordTextBox confirmPasswordBox = new PasswordTextBox();
		Button changeButton = new Button("Change Password");
		Button cancelButton = new Button("Cancel");
		
		oldPasswordBox.setName("oldpassword");
		newPasswordBox.setName("newpassword");
		confirmPasswordBox.setName("confirmpassword");
		
		
		changePasswordGrid.setWidget(0, 0, oldPassword);
		changePasswordGrid.setWidget(0, 1, oldPasswordBox);
		changePasswordGrid.setWidget(1, 0, newPassword);
		changePasswordGrid.setWidget(1, 1, newPasswordBox);
		changePasswordGrid.setWidget(2, 0, confirmPassword);
		changePasswordGrid.setWidget(2, 1, confirmPasswordBox);
		changePasswordGrid.setWidget(3, 0, changeButton);
		changePasswordGrid.setWidget(3, 1, cancelButton);
		
		changePassword.add(changePasswordGrid);
		accountManagementPanel.setWidget(changePassword);
		
		changeButton.addClickHandler(new ClickHandler() {

			@Override
			public void onClick(ClickEvent event) {
				if (newPasswordBox.getText().isEmpty()||newPasswordBox.getText().isEmpty()) {
					Window.alert("Please check the new password");
					return;
				}
				
				if (!newPasswordBox.getText().equals(confirmPasswordBox.getText())) {
					Window.alert("Please confirm the new password");
					return;
				}
				if(!oldPasswordBox.getText().equals("")){//TODO
					Window.alert("Please check the old password");
					return;
				}
				changePassword.submit();
				accountManagementPanel.setVisible(false);
			}

		});
		
		cancelButton.addClickHandler(new ClickHandler() {

			@Override
			public void onClick(ClickEvent event) {
				accountManagementPanel.setVisible(false);
			}
		});

		changePassword.addSubmitHandler(new FormPanel.SubmitHandler() {

			@Override
			public void onSubmit(SubmitEvent event) {
				;

			}
		});

		changePassword
				.addSubmitCompleteHandler(new FormPanel.SubmitCompleteHandler() {

					@Override
					public void onSubmitComplete(SubmitCompleteEvent event) {
						Window.alert("Password changed");
				}
	});
}
}
