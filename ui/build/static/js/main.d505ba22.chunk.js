(this.webpackJsonpui=this.webpackJsonpui||[]).push([[0],{14:function(e,t,n){e.exports=n(25)},19:function(e,t,n){},25:function(e,t,n){"use strict";n.r(t);var a=n(1),o=n.n(a),c=n(5),r=n.n(c),i=(n(19),n(6)),l=n(7),s=n(12),u=n(8),m=n(13),h=n(9),f=n(10),p=n(11),g=function(e){function t(){var e,n;Object(i.a)(this,t);for(var a=arguments.length,o=new Array(a),c=0;c<a;c++)o[c]=arguments[c];return(n=Object(s.a)(this,(e=Object(u.a)(t)).call.apply(e,[this].concat(o)))).state={fetching:!0,packets:[]},n}return Object(m.a)(t,e),Object(l.a)(t,[{key:"getReferenceURL",value:function(){var e=window.location;return e.protocol+"//"+e.host}},{key:"componentDidMount",value:function(){var e=this,t=window.location,n=t.pathname,a=t.protocol+"//"+t.host+"/gen/"+n.slice(1);console.log(a),fetch(a).then((function(e){return e.json()})).then((function(t){console.log(t),e.setState({fetching:!1,packets:t.sample})})).catch((function(t){console.log(t),e.setState({fetching:!1})}))}},{key:"render",value:function(){if(!0===this.state.fetching)return null;var e=o.a.createElement("span",{className:"notify-badge bottom blue"},o.a.createElement(f.a,{icon:p.a}));return o.a.createElement("div",null,this.state.packets.map((function(t){return o.a.createElement("div",{className:"search-result"},o.a.createElement(h.a,{trigger:e,position:"left center",modal:!0},o.a.createElement("div",null,o.a.createElement("ul",null," ",t.sources.map((function(e){return o.a.createElement("li",null,e)}))," "))),o.a.createElement("a",{href:t.refURL},o.a.createElement("span",{className:"notify-badge top red"},t.duplicates+"x"),o.a.createElement("img",{key:t.imgPath,src:t.imgPath})))})))}}]),t}(o.a.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));r.a.render(o.a.createElement(g,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[14,1,2]]]);
//# sourceMappingURL=main.d505ba22.chunk.js.map