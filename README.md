<table>
  <tr>
    <td>
      <img width="500px" src="https://render.fineartamerica.com/images/rendered/default/greeting-card/images/artworkimages/medium/2/northern-hawk-owl-hunting-peter-stahl.jpg"></img>
    </td>
    <td>
      <img width="400px" src="https://www.nmc.edu/news/2013/03/hawkowl.png"></img>
    </td>
  </tr>
</table>

# Concepts

- A client expresses a desire to perform some sort of immigration operation by creating a `Move`.

- A `Move` specifies the host country, and the dates, and may also specify the activity to be performed, the applicant's nationalities, payroll/contract location, etc.

- The objective is to find one or more `Processes` which can be used to effect this `Move`.
  A `Process` is an immigration `Route`, together with a list of `ProcessSteps`.

- A `Route` is simply a host country, together with a specific type of immigration permission.
  For example, "Work and Residence Permit in Ethiopia" might be a `Route`.

- When searching for matching `Processes`, Owldock consults its internal database of `ProcessRuleSets`.

- A `ProcessRuleSet` is a `Route`, and a collection of `ProcessSteps`, together with various criteria determining whether it matches a given `Move`.
  For example, "Move payroll must be in host country" could be a criterion associated with a `ProcessRuleSet`.

- A `Move` is defined to _match_ a `ProcessRuleSet` if the `Move` satisfies all of the criteria.

- In addition to the criteria, a `ProcessRuleSet` has rules determining which steps would be included for a given `Move`.
  For example, a step might only be required if the `Move` is for an applicant who is not a national of an EU country.

- When a match is found, we construct a `Process` for that match.
  The `Process` consists of (a) the `Route` from the `ProcessRuleSet`, and (b) the list of `ProcessSteps` which are required for this `Move`

- The client is then told that this `Route` can be used for their desired immigration operation, and that these are the steps that would be required.
  They could then proceed to initiate a `Case` using the selected `Process`.

- It is possible that Owldock will find multiple `Processes` for a given `Move`.

# Owldock development

Owldock consists of a javascript app implemented in [Vue.js](https://vuejs.org/), a backend application implemented in [Django](https://www.djangoproject.com/), and a [Postgres](https://www.postgresql.org/) database.
The UI uses the [Bulma](https://bulma.io/) css framework.

There are two modes of local development: "ui dev mode" and "realistic mode".

## 1. UI dev mode

In UI dev mode, the javascript client is running in a page served by a node.js dev server; not Django.
This means that the UI updates immediately when you edit javascript/css etc files.
In addition to the node.js dev server, we must run the Django server also, since it is needed to handle the Ajax requests made by the javascript.
This mode differs from how Owldock is run in production in various ways (e.g. in the way that Ajax requests are authenticated).

**Instructions:**

1. Edit `backend/owldock/settings/dev.py` so that `UI_DEV_MODE = True`
2. In one terminal: `cd backend && make serve`
3. In another terminal: `cd ui && make serve`

## 2. Realistic mode

This mode resembles how Owldock will be deployed in production.
All the javascript and css are bundled together and served by Django as "static files".
The downside of this mode is that, if you edit the javascript or css, you must rebuild the bundle (`make build`), which takes several seconds.

**Instructions:**

1. In one terminal: `cd ui && make build`
2. In another terminal: `cd backend && make serve`

# Running the Cypress tests

Install [Cypress](https://www.cypress.io/).

1. Ensure that `dev-mode.ts` is not imported in `ui/src/main.ts`
2. Set `UI_DEV_MODE = False` in `owldock/settings/dev.py`
3. `cd ui && make build`
4. `cd backend && make serve`
5. `cd ui && make test-live`. The Cypress app will launch.

The UI dev mode node.js server does not need to be running; just Django.
