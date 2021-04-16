/// <reference types="Cypress" />

describe("Case lifecycle", () => {
  it("Case can be managed by client and provider contacts", () => {
    // Log in as client contact
    cy.visit("/");
    cy.get("input[type='email']").type("petra-pepsi@example.com");
    cy.get("input[type='password']").type("x");
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
    cy.contains("Submit").click();

    // We are now in the active cases list view
    // Go to case detail view
    cy.wait(2000);
    cy.contains("Samantha Taylor").dblclick();

    // TODO: Take some actions as client contact

    // Log in as client contact

    cy.get("a.navbar-burger").click();
    // cy.contains("petra-pepsi@example.com").click({ force: true });
    cy.contains("Log out").click();

    cy.get("input[type='email']").type("dietrich-deloitte@example.com");
    cy.get("input[type='password']").type("x");
    cy.contains("Sign in").click();

    // Go to client portal and create case
    cy.visit("/portal");
    cy.contains("View active cases").click();

    // Go to case detail view
    cy.wait(2000);
    cy.contains("Samantha Taylor").dblclick();

    // TODO: Take some actions as provider contact
  });
});
