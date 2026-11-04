// Run480 exact conditional McNemar power. Node.js, no dependencies.
// Pre-specified conditional discordance counts, not a random-D power calculation.
function cdf(k,n,p) {
 if(k<0)return 0;
 const lf=[0];for(let i=1;i<=n;i++)lf[i]=lf[i-1]+Math.log(i);
 let v=[];for(let x=0;x<=k;x++)v.push(lf[n]-lf[x]-lf[n-x]+x*Math.log(p)+(n-x)*Math.log(1-p));
 const m=Math.max(...v);return Math.exp(m)*v.reduce((s,x)=>s+Math.exp(x-m),0);
}
function trial(n,d,p) {
 let k=0;while(2*cdf(k,d,.5)<=.05)k++;k--;
 return {n,d,p,critical_lower:k,critical_upper:d-k,
 power:cdf(k,d,p)+1-cdf(d-k-1,d,p)};
}
const cases=[[306,92,.65],[681,204,.60],[306,92,.60],[681,204,.65]];
const result=cases.map(v=>trial(...v));
console.log(JSON.stringify(result,null,2));
if(Math.abs(result[0].power-.8267077284451452)>1e-9)throw Error("unexpected output");
if(Math.abs(result[1].power-.8008053564450672)>1e-9)throw Error("unexpected output");
