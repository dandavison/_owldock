(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-0918e634"],{"05d8":function(e,t,a){"use strict";var n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("b-tabs",{model:{value:e.activeTab,callback:function(t){e.activeTab=t},expression:"activeTab"}},[a("b-tab-item",{attrs:{label:"All"}},[a("case-table",{attrs:{rows:e.rows,selected:e.selected,focusable:!0,columnSpec:{provider:{visible:!0}},paginated:!0},on:{"update:selected":function(t){e.selected=t},dblclick:e.navigateToRowDetailView}})],1),a("b-tab-item",{attrs:{label:"Selected"}},[e.isGenuineCaseObject(e.selected)?a("case",{attrs:{case_:e.selected}}):e._e()],1)],1)],1)},r=[],c=a("1da1"),s=(a("96cf"),a("b0c0"),a("2b0e")),i=a("888a"),o=a("035d"),u=a("0abd"),l=a("17fd"),d=a("6cff"),b=a("410c"),f=s["default"].extend({props:{role:String},components:{Case:o["a"],CaseTable:d["a"]},data:function(){return{activeTab:0,rows:[],selected:{},processIsNull:u["g"],Role:i["a"],routeName:this.$route.name}},created:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:e.fetchCaseList();case 1:case"end":return t.stop()}}),t)})))()},mounted:function(){var e=this;document.addEventListener("keydown",(function(t){"ArrowRight"===t.code||"Enter"===t.code?(b["a"].$emit("update:route-name-override","Case ".concat(e.selected.id||"")),e.activeTab=1):"ArrowLeft"===t.code&&(e.activeTab=0,b["a"].$emit("update:route-name-override",null),e.$nextTick((function(){var t;return null===(t=e.$el.querySelector("table"))||void 0===t?void 0:t.focus()})))}))},methods:{fetchCaseList:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){var a;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:t.t0=e.role,t.next=t.t0===i["a"].ClientContact?3:t.t0===i["a"].ProviderContact?5:t.t0===i["a"].Invalid?7:8;break;case 3:return a="/api/client-contact/list-cases/",t.abrupt("break",8);case 5:return a="/api/provider-contact/list-cases/",t.abrupt("break",8);case 7:return t.abrupt("return");case 8:return t.next=10,l["a"].fetchDataOrNull(a);case 10:if(t.t1=t.sent,t.t1){t.next=13;break}t.t1=[];case 13:e.rows=t.t1;case 14:case"end":return t.stop()}}),t)})))()},navigateToRowDetailView:function(e){this.$router.push("/portal/case/".concat(e.uuid))},isGenuineCaseObject:function(e){return!!e.applicant}}}),p=f,v=a("2877"),m=Object(v["a"])(p,n,r,!1,null,null,null);t["a"]=m.exports},e19c:function(e,t,a){"use strict";a.r(t);var n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"section"},[a("case-list",{attrs:{role:e.Role.ClientContact}})],1)},r=[],c=a("2b0e"),s=a("888a"),i=a("05d8"),o=c["default"].extend({components:{CaseList:i["a"]},data:function(){return{Role:s["a"]}}}),u=o,l=a("2877"),d=Object(l["a"])(u,n,r,!1,null,null,null);t["default"]=d.exports}}]);
//# sourceMappingURL=chunk-0918e634.2317a97d.js.map