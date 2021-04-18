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

function allStepsEarmarkedAssertions(params) {
  // Provider cannot see the case
  logOut();
  logIn(params.providerContactEmail, params.password);
  assertCaseNotInProviderListView(params);
}

function earmarkProviderOnFirstStep(params) {
  // Log back in as client user and select provider on a case step
  logOut();
  logIn(params.clientContactEmail, params.password);
  cy.contains("View active cases").click();

  // Go to a case detail view
  cy.contains(params.applicantName).dblclick();

  cy.contains("Select Provider")
    .first()
    .click();
  cy.contains("Waiting for user to notify provider").should("exist");
}

function notifyProviderOnFirstStep(params) {
  // Log back in as client user and select provider on a case step
  logOut();
  logIn(params.clientContactEmail, params.password);
  cy.contains("View active cases").click();

  // Go to a case detail view
  cy.contains(params.applicantName).dblclick();

  cy.contains("Notify Provider")
    .first()
    .click();
  cy.contains("Waiting for user to notify provider").should("exist");
}

function testCaseLifeCycle(params) {
  // We are in the cases list view and the table is populated.

  allStepsEarmarkedAssertions(params);

  earmarkProviderOnFirstStep(params);

  notifyProviderOnFirstStep(params);

  // Log back in as client user and select provider on a case step
  logOut();
  logIn(params.clientContactEmail, params.password);
  cy.contains("View active cases").click();

  // Go to a case detail view
  cy.contains(params.applicantName).dblclick();

  cy.contains("Select Provider")
    .first()
    .click();
  cy.contains("Waiting for provider to accept").should("exist");

  // Provider still cannot see the case
  logOut();
  logIn(params.providerContactEmail, params.password);
  assertCaseNotInProviderListView(params);

  // logIn(providerContactEmail, password);

  // // Go to provider portal
  // cy.visit("/portal");
  // cy.contains("View active cases").click();

  // cy.wait("@providerContactListCasesRequest").then(() => {
  //   // Go to case detail view
  //   cy.get("@applicantName").then(name => {
  //     cy.contains(name).dblclick();
  //     // TODO: Take some actions as provider contact
  //   });
  // });
}

function assertCaseInProviderListView(params) {
  cy.visit("/portal");
  cy.contains("View active cases").click();

  cy.wait("@providerContactListCasesRequest").then(() => {
    cy.contains(params.applicantName).should("exist");
  });
}

function assertCaseNotInProviderListView(params) {
  cy.visit("/portal");
  cy.contains("View active cases").click();
  cy.wait("@providerContactListCasesRequest").then(() => {
    cy.contains(params.applicantName).should("not.exist");
  });
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
  cy.visit("/portal");
  cy.contains("Initiate new work").click();
  // Select an applicant
  cy.get(".applicant-selector input").click();
  cy.get(".applicant-selector .dropdown-item")
    .first()
    .click()
    .invoke("text")
    .then(name =>
      Cypress._.trim(name)
        .split(" ")
        .slice(1)
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
