/* NPS Survey CX OS score dial: the same gauge customers see in the product.
   Vector SVG, sharp at any size (1080p, 4K, print).
   window.NPSDial.svg({kind:"nps"|"csat"|"ces", value:Number, size:px, dark:bool, label:bool}) returns an SVG string.
   Meaning colours come from the product dial: red #EB6665, track #E7E7E7, teal #267A72, needle #687385. */
(function(){
  var C={bad:"#EB6665",track:"#E7E7E7",good:"#267A72",needle:"#687385",ink:"#0F1A3D",muted:"#5A6787"};
  var K={
    nps:{min:-100,max:100,bands:[[-100,0,"bad"],[0,30,"track"],[30,100,"good"]],fmt:function(v){return (v>0?"+":"")+Math.round(v)},ends:["-100","100"],mid:"0",cap:"NPS"},
    csat:{min:0,max:100,bands:[[0,60,"bad"],[60,80,"track"],[80,100,"good"]],fmt:function(v){return Math.round(v)+"%"},ends:["0","100"],mid:"50",cap:"CSAT"},
    rate:{min:0,max:100,bands:[[0,20,"bad"],[20,30,"track"],[30,100,"good"]],fmt:function(v){return Math.round(v)+"%"},ends:["0","100"],mid:"50",cap:"Response rate"},
    health:{min:0,max:100,bands:[[0,40,"bad"],[40,70,"track"],[70,100,"good"]],fmt:function(v){return Math.round(v)+""},ends:["0","100"],mid:"50",cap:"Experience health"},
    score:{min:0,max:10,bands:[[0,7,"bad"],[7,9,"track"],[9,10,"good"]],fmt:function(v){return Math.round(v)+""},ends:["0","10"],mid:"5",cap:"Latest NPS answer"},
    ces:{min:1,max:7,bands:[[1,4,"bad"],[4,5,"track"],[5,7,"good"]],fmt:function(v){return v.toFixed(1)},ends:["1","7"],mid:"4",cap:"CES, out of 7"}
  };
  var A0=225,SW=270; /* start angle (deg, clockwise from 3 o'clock is 0, we use math angles) */
  function ang(k,v){return A0-SW*(v-k.min)/(k.max-k.min)}
  function pt(cx,cy,r,a){var t=a*Math.PI/180;return [cx+r*Math.cos(t),cy-r*Math.sin(t)]}
  function arc(cx,cy,r,a1,a2){var p1=pt(cx,cy,r,a1),p2=pt(cx,cy,r,a2),large=(a1-a2)>180?1:0;
    return "M"+p1[0].toFixed(2)+" "+p1[1].toFixed(2)+" A"+r+" "+r+" 0 "+large+" 1 "+p2[0].toFixed(2)+" "+p2[1].toFixed(2)}
  function svg(o){
    var k=K[o.kind||"nps"],v=Math.max(k.min,Math.min(k.max,o.value)),S=o.size||240,dark=!!o.dark;
    var cx=100,cy=100,r=78,w=16,out=[];
    out.push('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 '+(o.label===false?176:196)+'" width="'+S+'" role="img" aria-label="'+k.cap+' '+k.fmt(v)+'">');
    k.bands.forEach(function(b){out.push('<path d="'+arc(cx,cy,r,ang(k,b[0]),ang(k,b[1]))+'" fill="none" stroke="'+(dark&&b[2]=="track"?"rgba(255,255,255,.22)":C[b[2]])+'" stroke-width="'+w+'"/>')});
    for(var i=0;i<=20;i++){var a=A0-SW*i/20,p1=pt(cx,cy,r-w/2+1,a),p2=pt(cx,cy,r-w/2+(i%5?5:8),a);
      out.push('<line x1="'+p1[0].toFixed(2)+'" y1="'+p1[1].toFixed(2)+'" x2="'+p2[0].toFixed(2)+'" y2="'+p2[1].toFixed(2)+'" stroke="#fff" stroke-opacity=".85" stroke-width="'+(i%5?.8:1.3)+'"/>')}
    var ti=dark?"rgba(255,255,255,.7)":C.muted,f='font-family="IBM Plex Sans,system-ui,sans-serif"';
    var e1=pt(cx,cy,r+3,A0-4),e2=pt(cx,cy,r+3,A0-SW+4),m=pt(cx,cy,r+w/2+6,90);
    out.push('<text x="'+(e1[0]-4).toFixed(1)+'" y="'+(e1[1]+15).toFixed(1)+'" '+f+' font-size="8" fill="'+ti+'" text-anchor="middle">'+k.ends[0]+'</text>');
    out.push('<text x="'+(e2[0]+4).toFixed(1)+'" y="'+(e2[1]+15).toFixed(1)+'" '+f+' font-size="8" fill="'+ti+'" text-anchor="middle">'+k.ends[1]+'</text>');
    out.push('<text x="'+m[0].toFixed(1)+'" y="'+(m[1]+2).toFixed(1)+'" '+f+' font-size="8" fill="'+ti+'" text-anchor="middle">'+k.mid+'</text>');
    var a=ang(k,v),tip=pt(cx,cy,r-22,a),b1=pt(cx,cy,5.5,a+90),b2=pt(cx,cy,5.5,a-90);
    out.push('<g class="npsd-needle" style="transform-origin:100px 100px;--sw:'+(-(A0-a)).toFixed(1)+'deg"><path d="M'+b1[0].toFixed(2)+' '+b1[1].toFixed(2)+' L'+tip[0].toFixed(2)+' '+tip[1].toFixed(2)+' L'+b2[0].toFixed(2)+' '+b2[1].toFixed(2)+' Z" fill="'+(dark?"#C7D5FF":C.needle)+'"/><circle cx="100" cy="100" r="7" fill="'+(dark?"#C7D5FF":C.needle)+'"/></g>');
    out.push('<text x="100" y="150" '+f+' font-size="34" font-weight="600" fill="'+(dark?"#fff":C.ink)+'" text-anchor="middle" letter-spacing="-.5">'+k.fmt(v)+'</text>');
    if(o.label!==false)out.push('<text x="100" y="190" '+f+' font-size="11" fill="'+ti+'" text-anchor="middle">'+(o.caption||k.cap)+'</text>');
    out.push('</svg>');return out.join("");
  }
  function hydrate(root){(root||document).querySelectorAll("[data-dial]").forEach(function(el){var p=el.getAttribute("data-dial").split(":");
    el.innerHTML=svg({kind:p[0],value:parseFloat(p[1]),size:el.getAttribute("data-size")||240,dark:el.hasAttribute("data-dark"),caption:el.getAttribute("data-caption")||undefined});el.removeAttribute("data-dial");el.classList.add("npsd")})}
  window.NPSDial={svg:svg,colors:C,hydrate:hydrate};
  if(document.readyState!=="loading")hydrate();else document.addEventListener("DOMContentLoaded",function(){hydrate()});
})();
