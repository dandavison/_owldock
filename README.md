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
