(function(e){function n(n){for(var a,c,o=n[0],d=n[1],l=n[2],i=0,h=[];i<o.length;i++)c=o[i],Object.prototype.hasOwnProperty.call(r,c)&&r[c]&&h.push(r[c][0]),r[c]=0;for(a in d)Object.prototype.hasOwnProperty.call(d,a)&&(e[a]=d[a]);f&&f(n);while(h.length)h.shift()();return u.push.apply(u,l||[]),t()}function t(){for(var e,n=0;n<u.length;n++){for(var t=u[n],a=!0,c=1;c<t.length;c++){var o=t[c];0!==r[o]&&(a=!1)}a&&(u.splice(n--,1),e=d(d.s=t[0]))}return e}var a={},c={app:0},r={app:0},u=[];function o(e){return d.p+"js/"+({}[e]||e)+"."+{"chunk-247df7b1":"7af616f1","chunk-2ca0c5df":"4bb360e2","chunk-42c2f1a4":"444c1bc0","chunk-4f5356eb":"92b002fa","chunk-a2ce31f2":"20bc8258","chunk-58206dba":"bb1e1afb","chunk-2d21b12a":"d6999411","chunk-695afa1f":"c3fa47e6","chunk-0918e634":"89838458","chunk-091b22d2":"1dd6e299","chunk-2d0da3de":"2f263222","chunk-2d0e4aa1":"0454bc55","chunk-90920c3e":"439e30be","chunk-93524036":"975b0d51","chunk-5db9b45a":"4246bcaf","chunk-fc1bfbcc":"427c963f","chunk-2d0a31d5":"53103276","chunk-2d0abe6e":"436c1ab0","chunk-2d0b2774":"0d131fb9","chunk-2d0d7286":"1564017b","chunk-44dd306b":"1e9bee29","chunk-44dd4120":"a8ebbe0c","chunk-44de63f0":"06c3c4b7","chunk-44de9099":"b1a9fdb7"}[e]+".js"}function d(n){if(a[n])return a[n].exports;var t=a[n]={i:n,l:!1,exports:{}};return e[n].call(t.exports,t,t.exports,d),t.l=!0,t.exports}d.e=function(e){var n=[],t={"chunk-2ca0c5df":1,"chunk-4f5356eb":1,"chunk-58206dba":1,"chunk-695afa1f":1,"chunk-90920c3e":1,"chunk-93524036":1,"chunk-5db9b45a":1,"chunk-fc1bfbcc":1};c[e]?n.push(c[e]):0!==c[e]&&t[e]&&n.push(c[e]=new Promise((function(n,t){for(var a="css/"+({}[e]||e)+"."+{"chunk-247df7b1":"31d6cfe0","chunk-2ca0c5df":"26b1a075","chunk-42c2f1a4":"31d6cfe0","chunk-4f5356eb":"4beafa18","chunk-a2ce31f2":"31d6cfe0","chunk-58206dba":"007813df","chunk-2d21b12a":"31d6cfe0","chunk-695afa1f":"d3672360","chunk-0918e634":"31d6cfe0","chunk-091b22d2":"31d6cfe0","chunk-2d0da3de":"31d6cfe0","chunk-2d0e4aa1":"31d6cfe0","chunk-90920c3e":"ae23770a","chunk-93524036":"822ddcfa","chunk-5db9b45a":"4465b1c5","chunk-fc1bfbcc":"4465b1c5","chunk-2d0a31d5":"31d6cfe0","chunk-2d0abe6e":"31d6cfe0","chunk-2d0b2774":"31d6cfe0","chunk-2d0d7286":"31d6cfe0","chunk-44dd306b":"31d6cfe0","chunk-44dd4120":"31d6cfe0","chunk-44de63f0":"31d6cfe0","chunk-44de9099":"31d6cfe0"}[e]+".css",r=d.p+a,u=document.getElementsByTagName("link"),o=0;o<u.length;o++){var l=u[o],i=l.getAttribute("data-href")||l.getAttribute("href");if("stylesheet"===l.rel&&(i===a||i===r))return n()}var h=document.getElementsByTagName("style");for(o=0;o<h.length;o++){l=h[o],i=l.getAttribute("data-href");if(i===a||i===r)return n()}var f=document.createElement("link");f.rel="stylesheet",f.type="text/css",f.onload=n,f.onerror=function(n){var a=n&&n.target&&n.target.src||r,u=new Error("Loading CSS chunk "+e+" failed.\n("+a+")");u.code="CSS_CHUNK_LOAD_FAILED",u.request=a,delete c[e],f.parentNode.removeChild(f),t(u)},f.href=r;var s=document.getElementsByTagName("head")[0];s.appendChild(f)})).then((function(){c[e]=0})));var a=r[e];if(0!==a)if(a)n.push(a[2]);else{var u=new Promise((function(n,t){a=r[e]=[n,t]}));n.push(a[2]=u);var l,i=document.createElement("script");i.charset="utf-8",i.timeout=120,d.nc&&i.setAttribute("nonce",d.nc),i.src=o(e);var h=new Error;l=function(n){i.onerror=i.onload=null,clearTimeout(f);var t=r[e];if(0!==t){if(t){var a=n&&("load"===n.type?"missing":n.type),c=n&&n.target&&n.target.src;h.message="Loading chunk "+e+" failed.\n("+a+": "+c+")",h.name="ChunkLoadError",h.type=a,h.request=c,t[1](h)}r[e]=void 0}};var f=setTimeout((function(){l({type:"timeout",target:i})}),12e4);i.onerror=i.onload=l,document.head.appendChild(i)}return Promise.all(n)},d.m=e,d.c=a,d.d=function(e,n,t){d.o(e,n)||Object.defineProperty(e,n,{enumerable:!0,get:t})},d.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},d.t=function(e,n){if(1&n&&(e=d(e)),8&n)return e;if(4&n&&"object"===typeof e&&e&&e.__esModule)return e;var t=Object.create(null);if(d.r(t),Object.defineProperty(t,"default",{enumerable:!0,value:e}),2&n&&"string"!=typeof e)for(var a in e)d.d(t,a,function(n){return e[n]}.bind(null,a));return t},d.n=function(e){var n=e&&e.__esModule?function(){return e["default"]}:function(){return e};return d.d(n,"a",n),n},d.o=function(e,n){return Object.prototype.hasOwnProperty.call(e,n)},d.p="/static/",d.oe=function(e){throw console.error(e),e};var l=window["webpackJsonp"]=window["webpackJsonp"]||[],i=l.push.bind(l);l.push=n,l=l.slice();for(var h=0;h<l.length;h++)n(l[h]);var f=i;u.push([0,"chunk-vendors"]),t()})({0:function(e,n,t){e.exports=t("cd49")},"410c":function(e,n,t){"use strict";var a=t("2b0e"),c=new a["default"];n["a"]=c},"888a":function(e,n,t){"use strict";t.d(n,"a",(function(){return a})),t.d(n,"b",(function(){return u})),t.d(n,"c",(function(){return o})),t.d(n,"d",(function(){return d}));var a,c=t("a78e"),r=t.n(c);function u(){switch(r.a.get("role")){case"admin":return a.Admin;case"client-contact":return a.ClientContact;case"provider-contact":return a.ProviderContact;default:return a.Invalid}}function o(){return u()==a.Admin}function d(){return u()==a.ClientContact}(function(e){e["Admin"]="admin",e["ClientContact"]="client-contact",e["ProviderContact"]="provider-contact",e["Invalid"]="INVALID"})(a||(a={}))},cd49:function(e,n,t){"use strict";t.r(n);t("e260"),t("e6cf"),t("cca6"),t("a79d"),t("d3b7"),t("3ca3"),t("ddb0");var a=t("2b0e"),c=t("8c4f"),r=t("289d"),u=(t("5abe"),t("7051"),function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",{staticClass:"container"},[!1!==e.$route.meta.navbar?t("navbar"):e._e(),t("router-view")],1)}),o=[],d=function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("b-navbar",{attrs:{centered:""}},[t("template",{slot:"brand"},[t("b-navbar-item",[t("router-link",{attrs:{to:"/portal"}},[e.logoUrl?t("img",{attrs:{src:e.logoUrl,height:"24px"}}):e._e()])],1),t("b-navbar-item",[t("router-link",{attrs:{to:"/portal"}},[t("span",{staticStyle:{"font-size":"x-large"}},[e._v("🦉")]),e._v("Owldock ")])],1)],1),t("template",{slot:"start"},[t("b-navbar-item",[t("span",{staticClass:"route-name-override"},[e._v(e._s(e.routeNameOverride||e.$route.name))])])],1),t("template",{slot:"end"},[t("b-navbar-dropdown",{attrs:{label:e.loggedInUserName||"Account",arrowless:""}},[t("b-navbar-item",[t("a",{attrs:{href:e.logoutURL}},[e._v(" Log out ")])])],1)],1)],2)},l=[],i=t("a78e"),h=t.n(i),f=t("410c"),s=a["default"].extend({data:function(){return{currentViewTitle:"",routeNameOverride:""}},mounted:function(){var e=this;f["a"].$on("update:route-name-override",(function(n){e.routeNameOverride=n}))},computed:{logoutURL:function(){return"".concat("","/accounts/logout/")},loggedInUserName:function(){return h.a.get("username")},logoUrl:function(){return h.a.get("logo_url")}}}),b=s,p=(t("dea9"),t("2877")),k=Object(p["a"])(b,d,l,!1,null,"ed5dd718",null),m=k.exports,v=a["default"].extend({components:{Navbar:m}}),g=v,C=Object(p["a"])(g,u,o,!1,null,null,null),P=C.exports,w=t("888a");function y(){switch(Object(w["b"])()){case w["a"].ClientContact:return t.e("chunk-44de63f0").then(t.bind(null,"4938"));case w["a"].ProviderContact:return t.e("chunk-2d0abe6e").then(t.bind(null,"16f9"));default:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"))}}function O(){switch(Object(w["b"])()){case w["a"].ClientContact:return Promise.all([t.e("chunk-247df7b1"),t.e("chunk-a2ce31f2"),t.e("chunk-58206dba"),t.e("chunk-695afa1f"),t.e("chunk-2d0da3de")]).then(t.bind(null,"6b84"));case w["a"].ProviderContact:return Promise.all([t.e("chunk-247df7b1"),t.e("chunk-a2ce31f2"),t.e("chunk-58206dba"),t.e("chunk-695afa1f"),t.e("chunk-2d0e4aa1")]).then(t.bind(null,"90d8"));default:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"))}}function j(){switch(Object(w["b"])()){case w["a"].ClientContact:return Promise.all([t.e("chunk-247df7b1"),t.e("chunk-a2ce31f2"),t.e("chunk-58206dba"),t.e("chunk-695afa1f"),t.e("chunk-0918e634")]).then(t.bind(null,"e19c"));case w["a"].ProviderContact:return Promise.all([t.e("chunk-247df7b1"),t.e("chunk-a2ce31f2"),t.e("chunk-58206dba"),t.e("chunk-695afa1f"),t.e("chunk-091b22d2")]).then(t.bind(null,"aa29"));default:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"))}}function _(){switch(Object(w["b"])()){case w["a"].ClientContact:return Promise.all([t.e("chunk-247df7b1"),t.e("chunk-4f5356eb")]).then(t.bind(null,"47d3"));case w["a"].ProviderContact:return t.e("chunk-2d0abe6e").then(t.bind(null,"16f9"));default:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"))}}function A(){switch(Object(w["b"])()){case w["a"].ClientContact:return Promise.all([t.e("chunk-247df7b1"),t.e("chunk-a2ce31f2"),t.e("chunk-fc1bfbcc")]).then(t.bind(null,"1dcb"));case w["a"].ProviderContact:return Promise.all([t.e("chunk-247df7b1"),t.e("chunk-a2ce31f2"),t.e("chunk-5db9b45a")]).then(t.bind(null,"1c07"));default:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"))}}function x(){switch(Object(w["b"])()){case w["a"].ClientContact:return Promise.all([t.e("chunk-247df7b1"),t.e("chunk-a2ce31f2"),t.e("chunk-58206dba"),t.e("chunk-695afa1f"),t.e("chunk-90920c3e")]).then(t.bind(null,"d716"));case w["a"].ProviderContact:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"));default:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"))}}function E(){switch(Object(w["b"])()){case w["a"].ClientContact:return t.e("chunk-44de9099").then(t.bind(null,"3d02"));case w["a"].ProviderContact:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"));default:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"))}}function N(){switch(Object(w["b"])()){case w["a"].ClientContact:return t.e("chunk-44dd306b").then(t.bind(null,"0c4f"));case w["a"].ProviderContact:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"));default:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"))}}function I(){switch(Object(w["b"])()){case w["a"].ClientContact:return t.e("chunk-44dd4120").then(t.bind(null,"0fae"));case w["a"].ProviderContact:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"));default:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"))}}function S(){switch(Object(w["b"])()){case w["a"].ClientContact:return t.e("chunk-2d0d7286").then(t.bind(null,"762c"));case w["a"].ProviderContact:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"));default:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"))}}function L(){switch(Object(w["b"])()){case w["a"].Admin:return Promise.all([t.e("chunk-247df7b1"),t.e("chunk-a2ce31f2"),t.e("chunk-58206dba"),t.e("chunk-2ca0c5df"),t.e("chunk-2d21b12a")]).then(t.bind(null,"bde7"));default:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"))}}function T(){switch(Object(w["b"])()){case w["a"].Admin:return Promise.all([t.e("chunk-247df7b1"),t.e("chunk-2ca0c5df"),t.e("chunk-42c2f1a4")]).then(t.bind(null,"379b"));default:return t.e("chunk-2d0a31d5").then(t.bind(null,"0197"))}}a["default"].use(c["a"]);var M=function(){return t.e("chunk-2d0b2774").then(t.bind(null,"23da"))},U=function(){return Promise.all([t.e("chunk-247df7b1"),t.e("chunk-a2ce31f2"),t.e("chunk-58206dba"),t.e("chunk-695afa1f"),t.e("chunk-93524036")]).then(t.bind(null,"a388"))};a["default"].config.productionTip=!1,a["default"].use(r["a"],{defaultIconPack:"fas",defaultContainerElement:"#content"});var $=[{path:"/",component:y,name:"Home"},{path:"/portal",component:y,name:"Portal"},{path:"/portal/plan",component:E,name:"Plan"},{path:"/portal/initiate",component:N,name:"Initiate"},{path:"/portal/move",component:I,name:"Move"},{path:"/portal/report",component:S,name:"Report"},{path:"/portal/assessment",component:x,name:"Assessment"},{path:"/portal/my-data",component:M,name:"My Data"},{path:"/portal/new-case",component:U,name:"New Case"},{path:"/portal/cases",component:j,name:"My Cases"},{path:"/portal/case/:uuid",component:O,name:"Case"},{path:"/portal/applicants",component:A,name:"Applicants"},{path:"/portal/providers",component:_,name:"My Providers"},{path:"/portal/process/:id/steps/",component:T,name:"Process steps",props:!0},{path:"/portal/processes/:countryCode/",component:L,name:"Immigration Processes",props:!0},{path:"/portal/processes/:countryCode/:processIdString/",component:L,name:"Immigration Process",props:!0}],D=new c["a"]({mode:"history",routes:$});D.afterEach((function(){f["a"].$emit("update:route-name-override",null)})),new a["default"]({router:D,render:function(e){return e(P)}}).$mount("#app")},dea9:function(e,n,t){"use strict";t("fef6")},fef6:function(e,n,t){}});
//# sourceMappingURL=app.610abb4d.js.map