(this.webpackJsonpui=this.webpackJsonpui||[]).push([[0],{14:function(e,t,a){e.exports=a(26)},19:function(e,t,a){},25:function(e,t,a){},26:function(e,t,a){"use strict";a.r(t);var n=a(0),r=a.n(n),o=a(12),c=a.n(o),i=(a(19),a(2)),l=a(3),s=a(7),u=a(4),h=a(8),m=a(13),g=a(5),f=a(6),p=(a(25),function(e){function t(){return Object(i.a)(this,t),Object(s.a)(this,Object(u.a)(t).apply(this,arguments))}return Object(h.a)(t,e),Object(l.a)(t,[{key:"render",value:function(){var e=this.props.onAction;return r.a.createElement("div",{className:"buttonContainer",onClick:e},r.a.createElement("div",{className:"textAlignCenter colorWhite"},"...Click to Load More..."),r.a.createElement("div",{className:"textAlignCenter"},r.a.createElement(g.a,{icon:f.a,color:"white",size:"lg"})))}}]),t}(r.a.PureComponent)),v=function(e){function t(){var e,a;Object(i.a)(this,t);for(var n=arguments.length,r=new Array(n),o=0;o<n;o++)r[o]=arguments[o];return(a=Object(s.a)(this,(e=Object(u.a)(t)).call.apply(e,[this].concat(r)))).state={fetching:!0,packets:[],pageNumber:1,srcImage:""},a}return Object(h.a)(t,e),Object(l.a)(t,[{key:"getReferenceURL",value:function(){var e=window.location;return e.protocol+"//"+e.host}},{key:"getBaseURL",value:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:1,t=window.location,a=t.pathname,n=t.protocol,r=t.host,o=a.slice(1);0===o.length&&(o=this.state.srcImage);var c="?pageNumber="+e,i=n+"//"+r+"/gen/"+o,l=i+c;return console.log(l),l}},{key:"componentDidMount",value:function(){var e=this.getBaseURL();this.fetchData(e)}},{key:"fetchData",value:function(e){var t=this;fetch(e).then((function(e){return e.json()})).then((function(e){console.log(e);var a=e.sample,n=e.srcImage;t.setState({fetching:!1,packets:a,srcImage:n})})).catch((function(e){console.log(e),t.setState({fetching:!1})}))}},{key:"loadMore",value:function(){var e=this.getBaseURL(this.state.pageNumber+1);this.setState((function(e){return{pageNumber:e.pageNumber+1}})),this.fetchData(e)}},{key:"render",value:function(){var e=this,t=this.state,a=t.fetching,n=t.packets;if(!0===a)return null;var o=r.a.createElement("span",{className:"notify-badge top left blue"},r.a.createElement(g.a,{icon:f.b}));return r.a.createElement("div",null,n.map((function(e){return r.a.createElement("div",{className:"search-result",key:e.imgPath},r.a.createElement(m.a,{trigger:o,position:"left center",modal:!0},r.a.createElement("div",null,r.a.createElement("ul",null,e.sources.map((function(e){var t="http://web.archive.org/web/200910010000/"+e;return r.a.createElement("li",{key:e},r.a.createElement("a",{href:t,rel:"noopener noreferrer",target:"_blank"},e))}))))),r.a.createElement("a",{href:e.refURL},r.a.createElement("span",{className:"notify-badge top right red"},e.duplicates+"x"),r.a.createElement("img",{key:e.imgPath,src:e.imgPath,alt:e.imgPath})))})),r.a.createElement(p,{onAction:function(){return e.loadMore()}}))}}]),t}(r.a.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));c.a.render(r.a.createElement(v,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[14,1,2]]]);
//# sourceMappingURL=main.0fe42e69.chunk.js.map