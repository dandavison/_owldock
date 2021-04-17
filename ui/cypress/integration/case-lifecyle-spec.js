/// <reference types="Cypress" />

describe("Case lifecycle", () => {
  it("Case can be managed by client and provider contacts", () => {
    const password = "x";
    const clientContactEmail = "petra-pepsi@example.com";
    const providerContactEmail = "dietrich-deloitte@example.com";

    // Log in as client contact
    cy.visit("/");
    cy.get("input[type='email']").type(clientContactEmail);
    cy.get("input[type='password']").type(password);
    cy.contains("Sign in").click();

    // Go to client portal and create case
    cy.visit("/portal");
    cy.contains("Initiate new work").click();

    // Select an applicant
    cy.get(".applicant-selector input").click();
    cy.get(".applicant-selector .dropdown-item")
      .first()
      .click()
      .invoke("text")
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
    cy.intercept("/api/client-contact/list-cases/").as(
      "clientContactListCasesRequest"
    );
    cy.contains("Submit").click(); // redirects to cases list view

    cy.wait("@clientContactListCasesRequest").then(() => {
      // We are now in the cases list view and the table is populated.

      // Go to a case detail view
      cy.contains("Samantha Taylor").dblclick();

      // TODO: Take some actions as client contact
    });

    // Log in as client contact

    cy.get("a.navbar-burger").click();
    // cy.contains("petra-pepsi@example.com").click({ force: true });
    cy.contains("Log out").click();

    cy.get("input[type='email']").type(providerContactEmail);
    cy.get("input[type='password']").type(password);
    cy.contains("Sign in").click();

    // Go to client portal and create case
    cy.visit("/portal");
    cy.intercept("/api/provider-contact/list-cases/").as(
      "providerContactListCasesRequest"
    );
    cy.contains("View active cases").click();

    cy.wait("@providerContactListCasesRequest").then(() => {
      // Go to case detail view
      cy.contains("Samantha Taylor").dblclick();
      // TODO: Take some actions as provider contact
    });
  });
});
