/// <reference types="Cypress" />

describe("Case lifecycle", () => {
  it("Case can be managed by client and provider contacts", function() {
    const params = {
      clientContactEmail: "petra-pepsi@example.com",
      providerContactEmail: "dietrich-deloitte@example.com",
      password: "x"
    };

    cy.intercept("/api/client-contact/list-cases/").as(
      "clientContactListCasesRequest"
    );
    cy.intercept("/api/provider-contact/list-cases/").as(
      "providerContactListCasesRequest"
    );

    // Log in as client contact
    logIn(params.clientContactEmail, params.password);

    createCase();
    cy.wait("@clientContactListCasesRequest").then(() => {
      // We are now in the cases list view and the table is populated.
      params.applicantName = this.applicantName;
      testCaseLifeCycle(params);
    });
  });
});

function testCaseLifeCycle(params) {
  // We are in the cases list view and the table is populated.
  assertAllStepsEarmarked(params);
  assertProviderCannotSeeCase(params);
  earmarkProviderOnFirstStep(params);
  assertProviderCannotSeeCase(params);
  notifyProviderOnFirstStep(params);
  assertProviderCanSeeCase(params);
  providerRejectFirstCaseStep(params);
  assertProviderCannotSeeCase(params); // first step was only assigned step
  earmarkProviderOnFirstStep(params);
  notifyProviderOnFirstStep(params);
  assertProviderCanSeeCase(params);
  providerAcceptFirstCaseStep(params);
}

function assertAllStepsEarmarked(params) {
  cy.log("assertAllStepsEarmarked");
  clientViewFirstCase(params);
  cy.contains("Waiting for user to notify provider").should("exist");
  cy.contains("Waiting for provider to accept").should("not.exist");
}

function earmarkProviderOnFirstStep(params) {
  cy.log("earmarkProviderOnFirstStep");
  // Log back in as client user and select provider on a case step
  clientViewFirstCase(params);

  cy.contains("Select Provider")
    .first()
    .click();
  cy.contains("Waiting for user to notify provider").should("exist");
  cy.contains("Waiting for provider to accept").should("not.exist");
}

function notifyProviderOnFirstStep(params) {
  cy.log("notifyProviderOnFirstStep");
  // Log back in as client user and select provider on a case step
  clientViewFirstCase(params);

  cy.contains("Notify Provider")
    .first()
    .click();
  cy.contains("Waiting for provider to accept").should("exist");
}

function providerRejectFirstCaseStep(params) {
  cy.log("providerRejectCaseStep");
  providerViewFirstCase(params);
  cy.contains("Reject")
    .first()
    .click();
}

function providerAcceptFirstCaseStep(params) {
  cy.log("providerAcceptCaseStep");
  providerViewFirstCase(params);
  cy.contains("Accept")
    .first()
    .click();
  cy.contains("In progress").should("exist");
}

function assertProviderCanSeeCase(params) {
  cy.log("assertProviderCanSeeCase");
  providerViewCases(params);

  cy.wait("@providerContactListCasesRequest").then(() => {
    cy.contains(params.applicantName).should("exist");
  });
}

function assertProviderCannotSeeCase(params) {
  cy.log("assertProviderCannotSeeCase");
  providerViewCases(params);
  cy.wait("@providerContactListCasesRequest").then(() => {
    cy.contains(params.applicantName).should("not.exist");
  });
}

function clientViewCases(params) {
  cy.log("clientViewCases");
  logOut();
  logIn(params.clientContactEmail, params.password);
  cy.contains("View active cases").click();
}

function providerViewCases(params) {
  cy.log("providerViewCases");
  logOut();
  logIn(params.providerContactEmail, params.password);
  cy.contains("View active cases").click();
}

function clientViewFirstCase(params) {
  cy.log("clientViewFirstCase");
  clientViewCases(params);
  cy.contains(params.applicantName).dblclick();
}

function providerViewFirstCase(params) {
  cy.log("providerViewFirstCase");
  providerViewCases(params);
  cy.contains(params.applicantName).dblclick();
}

function logIn(email, password) {
  cy.visit("/");
  cy.get("input[type='email']").type(email);
  cy.get("input[type='password']").type(password);
  cy.contains("Sign in").click();
}

function logOut() {
  cy.get("a.navbar-burger").click();
  cy.contains("Log out").click();
}

// Go to client portal and create case
function createCase() {
  cy.log("createCase");
  cy.visit("/portal");
  cy.contains("Initiate new work").click();
  // Select an applicant
  cy.get(".applicant-selector input").click();
  cy.get(".applicant-selector .dropdown-item")
    .first()
    .click()
    .invoke("text")
    .then(name =>
      // One or more flag characters come first.
      // Last two words are the name.
      Cypress._.trim(name)
        .split(" ")
        .slice(-2)
        .join(" ")
    )
    .as("applicantName");

  // Select a country
  cy.get(".country-selector input").click();
  cy.get(".country-selector .dropdown-item")
    .first()
    .click();

  // Select a date range
  cy.get(".date-range-selector .control")
    .first()
    .click();
  cy.get(".date-range-selector a.datepicker-cell")
    .contains("27")
    .click();
  cy.get(".date-range-selector a.datepicker-cell")
    .contains("28")
    .click();

  // Select a route
  cy.get(".route-selector input").click();
  cy.get(".route-selector .dropdown-item")
    .first()
    .click();

  // Select a provider contact
  cy.get(".provider-contact-selector input").click();
  cy.get(".provider-contact-selector .dropdown-item")
    .first()
    .click();

  // Submit the form
  cy.contains("Submit").click(); // redirects to cases list view
}
