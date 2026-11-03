/* ASCII Plasma Offline WebGL Effect (LiDAR Studio Edition)
 * Author duy nhất: Nguyễn Hồng Bảo Trân (MSSV: 26127470) - Giao diện Web (UI/UX).
 * Team: ae cây khế - Course: CSC00004 - Class: 26C05.
 */
"use strict";(()=>{function y(a){let i={};for(let c of Array.from(a.attributes))c.name.startsWith("data-aifx-")&&(i[c.name.slice(10)]=c.value);return i}var U=["/editor","/preview","/backgrounds","/debug/effects"],I="aidesigner.ai",X=new Set(["localhost","127.0.0.1"]);function $(a){if(!a)return!1;let i=a.toLowerCase();return X.has(i)?!0:i===I||i.endsWith("."+I)}function j(a){return a?U.some(i=>a===i||a.startsWith(i+"/")):!1}function L(a){if(!a)return!1;try{let i=new URL(a);return $(i.hostname)&&j(i.pathname)}catch{return!1}}(()=>{var k;if(typeof window=="undefined"||window.AIFX)return;let a=document.currentScript,i=(k=a==null?void 0:a.src)!=null?k:"https://cdn.aidesigner.ai/effects/runtime/v1.js",c=i.replace(/\/runtime\/v1\.js.*$/,""),w=i.indexOf("?"),S=w===-1?"":i.slice(w),R=(a==null?void 0:a.getAttribute("data-aifx-key"))||new URLSearchParams(S).get("key")||"",W="https://api.aidesigner.ai/api/v1/effects/license";function v(e){try{return e.location.href}catch{return""}}function F(){return[location.href,document.referrer,window.parent&&window.parent!==window?v(window.parent):"",window.top&&window.top!==window?v(window.top):""].some(L)}let M=!1;function N(){if(M||!document.body)return;M=!0;let e=document.createElement("div");e.setAttribute("data-aifx-wm","");let n=e.attachShadow({mode:"closed"});n.innerHTML='<a href="https://aidesigner.ai/?ref=effect-badge" target="_blank" rel="noopener nofollow ugc" style="position:fixed;bottom:16px;right:16px;z-index:2147483647;display:flex;align-items:center;gap:6px;padding:7px 12px;border-radius:8px;background:#fff;color:#111;font:500 13px/1 system-ui,sans-serif;text-decoration:none;box-shadow:0 2px 10px rgba(0,0,0,.15);border:1px solid #e5e5e5;">\u2728 Made in AIDesigner</a>',document.body.appendChild(e)}let T=!1;function H(){return;T||(T=!0,!F()&&fetch(W+"?key="+encodeURIComponent(R)).then(e=>e.ok?e.json():null).then(e=>{e&&e.watermark&&N()}).catch(()=>{}))}let g=new Map,l=new Set,s=new WeakMap,m=new Set,h=new WeakMap;function P(e){return;if(g.has(e)||l.has(e)||!/^[a-z0-9-]{1,64}$/.test(e))return;l.add(e);let n=document.createElement("script");n.src=`${c}/fx/${e}/v1.js${S}`,n.async=!0,n.onerror=()=>l.delete(e),document.head.appendChild(n)}function O(e){try{if(!(parseFloat(getComputedStyle(e).zIndex)<0))return;for(let r=e.parentElement;r&&r!==document.documentElement;r=r.parentElement){let o=getComputedStyle(r);if(o.isolation==="isolate"||o.position!=="static"&&o.zIndex!=="auto"||o.transform!=="none"||o.filter!=="none"||parseFloat(o.opacity)<1||o.mixBlendMode!=="normal")return}let t=e.parentElement;t&&(t.style.isolation="isolate",console.info("[aifx] isolated the host section of a negative z-index effect so body/html backgrounds cannot paint over it"))}catch{}}function d(e){var f,u;if(!e||e.nodeType!==1||s.has(e))return;let n=e.getAttribute("data-aifx");if(!n)return;let t=e,r=g.get(n);if(!r){m.add(e),P(n);return}m.delete(e),((u=(f=t.ownerDocument)==null?void 0:f.defaultView)!=null?u:window).getComputedStyle(t).position==="static"&&(t.style.position="absolute"),t.style.overflow="hidden",O(t);try{s.set(e,{slug:n,instance:r.mount(t,y(t))});let b=setTimeout(()=>{s.has(e)&&h.delete(e)},3e4);e.addEventListener("aifx:contextlost",()=>{var C;clearTimeout(b);let E=(C=h.get(e))!=null?C:0;if(p(e),E>=10)return;h.set(e,E+1);let z=Math.min(700*Math.pow(1.6,E),8e3);setTimeout(()=>{e.isConnected&&!document.hidden&&d(e)},z+Math.random()*600)},{once:!0})}catch(b){console.warn("[aifx] mount failed:",n,b)}}function p(e){let n=s.get(e);if(n){try{n.instance.destroy()}catch{}s.delete(e)}m.delete(e)}function x(e){var t;e.nodeType===1&&e.hasAttribute("data-aifx")&&d(e),(t=e.querySelectorAll)==null||t.call(e,"[data-aifx]").forEach(d)}window.AIFX={register(e,n){g.set(e,n),l.delete(e),m.forEach(t=>{t.isConnected&&t.getAttribute("data-aifx")===e&&d(t)})},rescan:()=>x(document)};let _=new MutationObserver(e=>{var n;for(let t of e){if(t.type==="attributes"&&t.target.nodeType===1){if(!((n=t.attributeName)!=null&&n.startsWith("data-aifx")))continue;let r=t.target;if(t.attributeName==="data-aifx")p(r),d(r);else{let o=s.get(r);if(o)try{o.instance.update(y(r))}catch{}}continue}t.addedNodes.forEach(r=>{r.nodeType===1&&x(r)}),t.removedNodes.forEach(r=>{var f,u;if(r.nodeType!==1)return;let o=r;(f=o.hasAttribute)!=null&&f.call(o,"data-aifx")&&p(o),(u=o.querySelectorAll)==null||u.call(o,"[data-aifx]").forEach(p)})}}),A=()=>{x(document),_.observe(document.documentElement,{childList:!0,subtree:!0,attributes:!0})};document.readyState==="loading"?document.addEventListener("DOMContentLoaded",A,{once:!0}):A()})();})();

"use strict";(()=>{var P=/^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$/;function T(o){let i=o.replace("#","");(i.length===3||i.length===4)&&(i=i.split("").map(e=>e+e).join("")),i.length===8&&(i=i.slice(0,6));let t=parseInt(i,16);return[(t>>16&255)/255,(t>>8&255)/255,(t&255)/255]}function A(o,i){let t={};for(let[e,l]of Object.entries(o)){let s=i[e];if(l.type==="number"){let f=s==null?NaN:parseFloat(s);t[e]=Number.isFinite(f)?Math.min(l.max,Math.max(l.min,f)):l.default}else if(l.type==="colors"){let f=(s!=null?s:"").split(",").map(u=>u.trim()).filter(u=>P.test(u));t[e]=f.length>=l.min?f.slice(0,l.max):l.default.slice()}else l.type==="enum"?t[e]=s!=null&&l.values.includes(s)?s:l.default:t[e]=s!=null&&/^https:\/\/[^\s"'<>]+$/i.test(s)?s:l.default}return t}var L="attribute vec2 a_pos;varying vec2 v_uv;void main(){v_uv=a_pos*0.5+0.5;gl_Position=vec4(a_pos,0.,1.);}";function q(){let o=typeof window!="undefined"?window.__AIFX_MAX_DPR__:void 0;return typeof o=="number"&&o>0?o:1.5}function M(o){try{let i=new URL(o);return i.protocol!=="https:"||i.hostname!=="cdn.aidesigner.ai"?null:`https://api.aidesigner.ai/api/v1/effects/image-proxy?url=${encodeURIComponent(o)}`}catch{return null}}function S(o,i){var y;let t=document.createElement("canvas");t.style.cssText="position:absolute;inset:0;width:100%;height:100%;display:block;";let e=(y=t.getContext("webgl",{alpha:!0,antialias:!1,premultipliedAlpha:!1}))!=null?y:t.getContext("experimental-webgl");if(!e)return null;function l(n,a){let r=e.createShader(n);return r?(e.shaderSource(r,a),e.compileShader(r),e.getShaderParameter(r,e.COMPILE_STATUS)?r:(console.warn("[aifx] shader compile failed:",e.getShaderInfoLog(r)),null)):null}let s=l(e.VERTEX_SHADER,L),f=l(e.FRAGMENT_SHADER,i),u=e.createProgram();if(!s||!f||!u)return null;if(e.attachShader(u,s),e.attachShader(u,f),e.linkProgram(u),!e.getProgramParameter(u,e.LINK_STATUS))return console.warn("[aifx] program link failed:",e.getProgramInfoLog(u)),null;e.useProgram(u),t.addEventListener("webglcontextlost",n=>{n.preventDefault(),o.dispatchEvent(new CustomEvent("aifx:contextlost"))});let _=e.createBuffer();e.bindBuffer(e.ARRAY_BUFFER,_),e.bufferData(e.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),e.STATIC_DRAW);let h=e.getAttribLocation(u,"a_pos");e.enableVertexAttribArray(h),e.vertexAttribPointer(h,2,e.FLOAT,!1,0,0),e.enable(e.BLEND),e.blendFunc(e.SRC_ALPHA,e.ONE_MINUS_SRC_ALPHA);let g=new Map;function v(n){var a;return g.has(n)||g.set(n,e.getUniformLocation(u,n)),(a=g.get(n))!=null?a:null}o.appendChild(t);let x=null,b=0,w=null,p={gl:e,canvas:t,setUniform1f:(n,a)=>{let r=v(n);r&&e.uniform1f(r,a)},setUniform2f:(n,a,r)=>{let m=v(n);m&&e.uniform2f(m,a,r)},setUniform3f:(n,a,r,m)=>{let c=v(n);c&&e.uniform3f(c,a,r,m)},setColor:(n,a)=>{let[r,m,c]=T(a);p.setUniform3f(n,r,m,c)},setImage:n=>{if(n===w)return;w=n;let a=++b;if(!n){p.setUniform1f("u_hasImage",0);return}let r=(m,c)=>{let d=new Image;d.crossOrigin="anonymous";let R=()=>{if(a!==b)return;let E=c?null:M(n);if(E){r(E,!0);return}w=null,p.setUniform1f("u_hasImage",0)};d.onload=()=>{if(a!==b)return;x||(x=e.createTexture()),e.activeTexture(e.TEXTURE0),e.bindTexture(e.TEXTURE_2D,x),e.pixelStorei(e.UNPACK_FLIP_Y_WEBGL,!0);try{e.texImage2D(e.TEXTURE_2D,0,e.RGBA,e.RGBA,e.UNSIGNED_BYTE,d)}catch{R();return}e.texParameteri(e.TEXTURE_2D,e.TEXTURE_WRAP_S,e.CLAMP_TO_EDGE),e.texParameteri(e.TEXTURE_2D,e.TEXTURE_WRAP_T,e.CLAMP_TO_EDGE),e.texParameteri(e.TEXTURE_2D,e.TEXTURE_MIN_FILTER,e.LINEAR),e.texParameteri(e.TEXTURE_2D,e.TEXTURE_MAG_FILTER,e.LINEAR);let E=v("u_image");E&&e.uniform1i(E,0),p.setUniform2f("u_imageRes",d.naturalWidth,d.naturalHeight),p.setUniform1f("u_hasImage",1)},d.onerror=R,d.src=m};r(n,!1)},draw:n=>{p.setUniform1f("u_time",n),e.drawArrays(e.TRIANGLES,0,3)},resize:()=>{let n=Math.min(window.devicePixelRatio||1,q()),a=Math.max(1,Math.round(o.clientWidth*n)),r=Math.max(1,Math.round(o.clientHeight*n));(t.width!==a||t.height!==r)&&(t.width=a,t.height=r,e.viewport(0,0,a,r),p.setUniform2f("u_res",a,r))},destroy:()=>{var n;t.remove();try{(n=e.getExtension("WEBGL_lose_context"))==null||n.loseContext()}catch{}}};return p.resize(),p}function U(o,i,t){let e=typeof matchMedia=="function"&&matchMedia("(prefers-reduced-motion: reduce)").matches,l=0,s=!0,f=performance.now(),u=.5,_=.5,h=.5,g=.5,v=0,x=-1e9,b=m=>{let c=o.getBoundingClientRect();c.width<1||c.height<1||(u=(m.clientX-c.left)/c.width,_=(m.clientY-c.top)/c.height,x=performance.now())};window.addEventListener("pointermove",b,{passive:!0});let w=typeof window.__AIFX_FPS_CAP__=="number"&&window.__AIFX_FPS_CAP__>0?window.__AIFX_FPS_CAP__:0,p=w>0?1e3/w-1:0,y=-1e9,n=()=>{!e&&s&&(l=requestAnimationFrame(n));let m=performance.now();if(m-y<p)return;y=m;let c=(m-f)/1e3;h+=(u-h)*.07,g+=(_-g)*.07,v+=((m-x<2500?1:0)-v)*.045;let d=o.clientWidth/Math.max(o.clientHeight,1);i.setUniform2f("u_mouse",h*d,1-g),i.setUniform1f("u_mouseAct",v),t(c),i.draw(c)},a=typeof IntersectionObserver=="function"?new IntersectionObserver(m=>{let c=m.some(d=>d.isIntersecting);c&&!s?(s=!0,l=requestAnimationFrame(n)):!c&&s&&(s=!1,cancelAnimationFrame(l))}):null;a==null||a.observe(o);let r=typeof ResizeObserver=="function"?new ResizeObserver(()=>i.resize()):null;return r==null||r.observe(o),l=requestAnimationFrame(n),()=>{cancelAnimationFrame(l),window.removeEventListener("pointermove",b),a==null||a.disconnect(),r==null||r.disconnect()}}function C(o,i){let t=document.createElement("div");return t.style.cssText=`position:absolute;inset:0;background:linear-gradient(135deg, ${i.join(", ")});opacity:.85;`,o.appendChild(t),()=>t.remove()}var F={colors:{type:"colors",default:["#0e4a30","#10b981","#6ee7b7"],min:1,max:4},bg:{type:"colors",default:["#09090b"],min:1,max:1},"bg-alpha":{type:"number",default:1,min:0,max:1},speed:{type:"number",default:.3,min:.05,max:2},"cell-size":{type:"number",default:18,min:8,max:36},levels:{type:"number",default:9,min:3,max:10},scale:{type:"number",default:1.6,min:.5,max:4},glow:{type:"number",default:.55,min:0,max:1},flicker:{type:"number",default:.3,min:0,max:1},contrast:{type:"number",default:1.15,min:.5,max:2.5},scanlines:{type:"number",default:.3,min:0,max:1}},X=`
precision highp float;
varying vec2 v_uv;
uniform vec2 u_res;
uniform float u_time,u_speed,u_cell,u_levels,u_scale,u_glow,u_flicker,u_contrast,u_scan,u_bgalpha,u_dpr,u_colorCount;
uniform vec3 u_bg,u_c0,u_c1,u_c2,u_c3;

float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453123);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);
  return mix(mix(hash(i),hash(i+vec2(1.,0.)),f.x),mix(hash(i+vec2(0.,1.)),hash(i+vec2(1.,1.)),f.x),f.y);}
float fbm(vec2 p){float v=0.0,a=0.5;for(int i=0;i<4;i++){v+=a*noise(p);p*=2.07;a*=0.5;}return v;}

vec3 ramp(float t){
  t=clamp(t,0.0,1.0)*(u_colorCount-1.0);
  if(t<1.0)return mix(u_c0,u_c1,t);
  if(t<2.0)return mix(u_c1,u_c2,t-1.0);
  return mix(u_c2,u_c3,t-2.0);
}

float sdBox(vec2 p,vec2 b){vec2 d=abs(p)-b;return length(max(d,0.0))+min(max(d.x,d.y),0.0);}
float sdSeg(vec2 p,vec2 a,vec2 b){vec2 pa=p-a,ba=b-a;float h=clamp(dot(pa,ba)/dot(ba,ba),0.0,1.0);return length(pa-ba*h);}

// procedural glyph SDF ramp:  (space) . : - = + * # @
float glyph(float gi,vec2 q){
  if(gi<0.5)return 1.0;
  if(gi<1.5)return length(q-vec2(0.0,-0.30))-0.16;
  if(gi<2.5)return min(length(q-vec2(0.0,0.28)),length(q-vec2(0.0,-0.28)))-0.15;
  if(gi<3.5)return sdBox(q,vec2(0.30,0.09));
  if(gi<4.5)return min(sdBox(q-vec2(0.0,0.19),vec2(0.30,0.085)),sdBox(q+vec2(0.0,0.19),vec2(0.30,0.085)));
  if(gi<5.5)return min(sdBox(q,vec2(0.32,0.09)),sdBox(q,vec2(0.09,0.32)));
  if(gi<6.5){
    float d=sdSeg(q,vec2(0.0,-0.32),vec2(0.0,0.32));
    d=min(d,sdSeg(q,vec2(-0.28,-0.16),vec2(0.28,0.16)));
    d=min(d,sdSeg(q,vec2(-0.28,0.16),vec2(0.28,-0.16)));
    return d-0.09;
  }
  if(gi<7.5){
    float d=min(sdBox(q-vec2(0.0,0.17),vec2(0.34,0.075)),sdBox(q+vec2(0.0,0.17),vec2(0.34,0.075)));
    return min(d,min(sdBox(q-vec2(0.15,0.0),vec2(0.075,0.36)),sdBox(q+vec2(0.15,0.0),vec2(0.075,0.36))));
  }
  float d=abs(length(q)-0.31)-0.08;
  return min(d,length(q)-0.13);
}

// cheap sin-interference plasma with orbiting sources (no noise) \u2014 reused for the glow wash
float plasma(vec2 p,float t){
  vec2 o1=vec2(0.55+0.4*sin(t*0.31),0.32*cos(t*0.23));
  vec2 o2=vec2(-0.5+0.35*cos(t*0.27),0.36*sin(t*0.19)-0.08);
  float v=sin(p.x*2.3-t*0.7)+sin(p.y*3.1+t*0.5)+sin((p.x+p.y)*1.9+t*0.6);
  v+=1.7*sin(length(p-o1)*3.6-t*0.9);
  v+=1.5*sin(length(p-o2)*3.1+t*0.8);
  v*=0.16;
  return v/(1.0+abs(v)*0.4); // gentle soft clip, stays in linear range for smooth gradation
}

void main(){
  float aspect=u_res.x/max(u_res.y,1.0);
  float t=u_time*u_speed;
  float cellH=max(u_cell*u_dpr,4.0);
  vec2 cellSz=vec2(cellH*0.62,cellH);
  vec2 px=v_uv*u_res;
  vec2 cellId=floor(px/cellSz);
  vec2 cellC=(cellId+0.5)*cellSz;
  vec2 q=(px-cellC)/cellH*2.0;          // physical cell-local coords, y in [-1,1]
  vec2 qn=(px-cellC)/cellSz*2.0;        // normalized cell-local coords for halo

  // --- field at cell center (crisp per-cell brightness) ---
  vec2 fp=(cellC/u_res.y-vec2(0.5*aspect,0.5))*u_scale;
  float pv=plasma(fp,t);
  float w=fbm(fp*2.1+vec2(t*0.10,-t*0.07)+pv*0.8);
  float vc=clamp(0.5+pv*0.95+(w-0.5)*0.45,0.0,1.0);
  vc=clamp(0.5+(vc-0.5)*u_contrast*1.25,0.0,1.0);
  vc=pow(vc,1.3); // deepen darks so forms float in negative space
  vc-=smoothstep(0.72,1.0,vc)*(0.02+0.20*(1.0-w)); // erode bright cores with fbm so they break into # * + textures

  // per-cell flicker (stepped time) + static dither to break level banding
  float fl=hash(cellId+floor(u_time*9.0));
  vc+=(fl-0.5)*u_flicker*0.10;
  vc+=(hash(cellId*1.7+11.3)-0.5)*(0.30/u_levels);
  // sparse blinking dots in the void \u2014 idle-terminal noise
  float spark=smoothstep(0.972,1.0,hash(cellId*2.3+floor(u_time*2.5)));
  vc=max(vc,spark*(0.35+0.5*u_flicker)/u_levels);
  vc=clamp(vc,0.0,1.0);

  // --- quantize to glyph ramp ---
  float lv=clamp(floor(vc*u_levels),0.0,u_levels-1.0);
  float den=max(u_levels-1.0,1.0);
  float gi=floor(lv/den*8.0+0.5);
  float vq=lv/den;

  float d=glyph(gi,q/1.4)*1.4; // glyphs fill ~70% of the cell like real terminal chars
  float aa=2.4/cellH;
  float cov=smoothstep(aa,-aa,d);

  // --- smooth phosphor wash (fragment-resolution, cheap plasma only) ---
  float pw=clamp(plasma((px/u_res.y-vec2(0.5*aspect,0.5))*u_scale,t)+0.5,0.0,1.0);
  pw=pw*pw;
  vec3 wash=ramp(pw*0.85)*pw*u_glow*0.16;

  // --- per-cell halo with exponential falloff ---
  float halo=exp(-dot(qn,qn)*1.1)*pow(vq,2.0)*u_glow*0.35;

  // --- glyph color ---
  vec3 gcol=ramp(mix(vq,vc,0.35));
  gcol*=0.62+0.6*vc;
  gcol=mix(gcol,vec3(1.0),smoothstep(0.86,1.0,vc)*0.3);

  // --- compose ---
  vec2 vctr=(v_uv-0.5)*vec2(aspect,1.0);
  float vig=1.0-0.28*smoothstep(0.3,1.1,length(vctr));
  vec3 col=u_bg*vig*u_bgalpha+wash+ramp(vq)*halo;
  col+=ramp(vc)*vc*0.05; // faint per-cell ambient tint for depth in empty cells
  col=mix(col,gcol,cov);

  // CRT scanlines (2 CSS px period) + slow refresh sweep
  float scan=1.0-u_scan*0.16*(0.5+0.5*sin(px.y/u_dpr*3.14159));
  col*=scan;
  float sp=fract(u_time*0.05);
  float dsw=(v_uv.y-(1.0-sp))*9.0;
  col*=1.0+exp(-dsw*dsw)*u_flicker*0.10;

  // film grain + dither
  col+=(hash(px*0.7+fract(u_time)*13.1)-0.5)*0.02;
  col+=(hash(px+0.5)-0.5)*0.008;

  float alpha=clamp(max(u_bgalpha,cov+halo*0.6+pw*u_glow*0.3),0.0,1.0);
  gl_FragColor=vec4(col,alpha);
}`,I;(I=window.AIFX)==null||I.register("ascii",{mount(o,i){let t=A(F,i),e=S(o,X);if(!e){let f=C(o,t.colors);return{update(){},destroy:f}}let l=()=>{let f=t.colors;e.setUniform1f("u_colorCount",f.length),["u_c0","u_c1","u_c2","u_c3"].forEach((u,_)=>e.setColor(u,f[Math.min(_,f.length-1)])),e.setColor("u_bg",t.bg[0]),e.setUniform1f("u_bgalpha",t["bg-alpha"]),e.setUniform1f("u_speed",t.speed),e.setUniform1f("u_cell",t["cell-size"]),e.setUniform1f("u_levels",t.levels),e.setUniform1f("u_scale",t.scale),e.setUniform1f("u_glow",t.glow),e.setUniform1f("u_flicker",t.flicker),e.setUniform1f("u_contrast",t.contrast),e.setUniform1f("u_scan",t.scanlines),e.setUniform1f("u_dpr",Math.min(window.devicePixelRatio||1,1.5))};l();let s=U(o,e,()=>{});return{update(f){t=A(F,f),l()},destroy(){s(),e.destroy()}}}});})();
