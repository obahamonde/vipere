import{d as B,T as E,r as N,a as l,o as r,c as i,u as o,b as $,t as v,e as n,w as c,f as p,g as b,h as T,F,i as O,j as G,k as H,l as C,m as K,n as P,p as A,q as Q}from"./index-77073553.js";const X={key:0,"dark:invert":"",br:"",fixed:"",sh:"","p-4":"",rounded:"","m-4":"","mr-96":""},Y=["src","alt"],Z=B({__name:"Auth",setup(D){const{user:f,isAuthenticated:t,loginWithRedirect:j,logout:V}=E(),k=N(!1);return(w,s)=>{const g=l("v-icon"),m=l("v-btn");return r(),i(F,null,[o(k)?(r(),i("div",X,[$("p",null,v(o(f).name),1),$("p",null,v(o(f).email),1),o(t)?(r(),i("button",{key:0,row:"",icon:"",onClick:s[0]||(s[0]=x=>o(V)()),text:"red","hover:text-red-700":""},[n(g,null,{default:c(()=>[p("mdi-logout")]),_:1}),p("Logout ")])):b("",!0)])):b("",!0),o(t)?b("",!0):(r(),T(m,{key:1,icon:"",onClick:s[1]||(s[1]=x=>o(j)()),x4:"","m-4":"",fixed:"",br:""},{default:c(()=>[n(g,null,{default:c(()=>[p("mdi-account")]),_:1})]),_:1})),$("div",{onClick:s[2]||(s[2]=x=>k.value=!o(k)),cp:"","m-4":"","mr-72":"",fixed:"",br:"","z-50":""},[o(t)?(r(),i("img",{key:0,src:o(f).picture,alt:o(f).name,rf:"",sh:"",x4:""},null,8,Y)):b("",!0)])],64)}}}),ee="/favicon.gif",ne=$("img",{src:ee,rf:"",x3:""},null,-1),te={key:0,cp:"",scale:"",row:"",center:""},oe={key:1,cp:"",scale:"",row:"",center:""},ce=["href"],le={key:2,cp:"",scale:"",row:"",center:""},ae={key:3,cp:"",scale:"",row:""},re={key:4,cp:"",scale:"",row:""},ie=B({__name:"editor",setup(D){const{getAccessTokenSilently:f}=E(),{state:t,dispatch:j}=O(),V=()=>{window.location.reload()},k=async()=>{const d=await f(),{data:u}=await C("https://dev-tvhqmk7a.us.auth0.com/userinfo",{headers:{Authorization:`Bearer ${d}`}}).json();t.user=o(u);const{data:h}=await C("/api/upload/"+t.user.sub).json();t.workspace=o(h)},w=async(d,u)=>{const{data:h}=await C("/api/upload/?key="+d.split("cdn.hatarini.com/")[1]).json();t.currentFolder={[u]:JSON.stringify(o(h))}},s=async d=>{t.codeUrl=d;const{data:u}=await C(t.codeUrl).text();t.code=o(u),t.currentname=t.codeUrl.split("lambda/")[1],await g()},g=async()=>{const{data:d}=await C("/api/download/?key="+t.codeUrl.split("cdn.hatarini.com/")[1]).json();t.code=o(d)},m=async d=>{await C("/api/upload/?key="+d.split("cdn.hatarini.com/")[1],{method:"DELETE"}),await k(),t.code=""},x=N([]);return G(async()=>{await k(),x.value=t.workspace}),H(async()=>{t.workspace?x.value=t.workspace:await k()}),(d,u)=>{const h=l("v-btn"),S=l("v-toolbar-title"),U=l("v-spacer"),q=l("v-icon"),z=l("v-app-bar"),_=l("Icon"),y=l("v-title"),L=l("v-list-item"),R=l("v-list"),I=l("v-navigation-drawer"),M=l("RouterView"),W=Z,J=l("v-main");return r(),i(F,null,[n(z,{app:"",color:o(A)?"secondary":"primary",dark:"",fixed:""},{default:c(()=>[n(h,{icon:"",onClick:u[0]||(u[0]=K(e=>V(),["stop"]))},{default:c(()=>[ne]),_:1}),n(S,{"font-script":"","hover:text-amber":"",cp:""},{default:c(()=>[p("Vipére")]),_:1}),n(U),n(h,{icon:"",onClick:u[1]||(u[1]=e=>o(P)())},{default:c(()=>[n(q,null,{default:c(()=>[p(v(o(A)?"mdi-lightbulb-on":"mdi-lightbulb"),1)]),_:1})]),_:1})]),_:1},8,["color"]),n(I,{app:"",clipped:"",fixed:"",width:"150",permanent:"",col:"",center:""},{default:c(()=>[n(R,{dense:""},{default:c(()=>[(r(!0),i(F,null,Q(o(t).workspace,e=>(r(),T(L,{key:e.title,link:""},{default:c(()=>[e.name.includes(".py")?(r(),i("div",te,[n(_,{icon:"logos:python","m-1":"",onClick:a=>s(e.url)},null,8,["onClick"]),n(y,{"text-xs":"",onClick:a=>s(e.url)},{default:c(()=>[p(v(e.name),1)]),_:2},1032,["onClick"]),n(_,{icon:"mdi-delete",onClick:a=>m(e.url),"text-red":"","hover:text-red-700":""},null,8,["onClick"])])):e.name.includes(".html")?(r(),i("div",oe,[n(_,{icon:"logos:html-5","m-1":"",onClick:a=>s(e.url)},null,8,["onClick"]),n(y,{"text-xs":""},{default:c(()=>[$("a",{href:e.url,"decoration-none":""},v(e.name),9,ce)]),_:2},1024),n(_,{icon:"mdi-delete",onClick:a=>m(e.url),"text-red":"","hover:text-red-700":""},null,8,["onClick"])])):e.name.includes("requirements.txt")?(r(),i("div",le,[n(_,{icon:"mdi-cog",onClick:a=>s(e.url)},null,8,["onClick"]),n(y,{"text-xs":"",onClick:a=>s(e.url)},{default:c(()=>[p(v(e.name),1)]),_:2},1032,["onClick"]),n(_,{icon:"mdi-delete",onClick:a=>m(e.url),"text-red":"","hover:text-red-700":""},null,8,["onClick"])])):e.type==="directory"?(r(),i("div",ae,[n(_,{icon:"mdi-folder",onClick:a=>w(e.url,e.name)},null,8,["onClick"]),n(y,{onClick:a=>w(e.url,e.name)},{default:c(()=>[p(v(e.name),1)]),_:2},1032,["onClick"]),n(_,{icon:"mdi-delete",onClick:a=>m(e.url),"text-red":"","hover:text-red-700":""},null,8,["onClick"])])):(r(),i("div",re,[n(_,{icon:"mdi-file",onClick:a=>w(e.url,e.name)},null,8,["onClick"]),n(y,{onClick:a=>w(e.url,e.name)},{default:c(()=>[p(v(e.name),1)]),_:2},1032,["onClick"]),n(_,{icon:"mdi-delete",onClick:a=>m(e.url),"text-red":"","hover:text-red-700":""},null,8,["onClick"])]))]),_:2},1024))),128))]),_:1})]),_:1}),n(J,null,{default:c(()=>[n(M),n(W,{"z-50":""})]),_:1})],64)}}});export{ie as default};