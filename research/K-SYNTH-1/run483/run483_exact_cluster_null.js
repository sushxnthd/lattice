// Run483: exact null enumeration. Node.js, no dependencies.
"use strict";
const R=5, M=3, alpha=0.05;
function choose(n,k){let x=1;for(let i=1;i<=k;i++)x=x*(n-i+1)/i;return x;}
function pval(a,b){const n=a+b,k=Math.min(a,b);let s=0;for(let i=0;i<=k;i++)s+=choose(n,i)/2**n;return Math.min(1,2*s);}
const rows=[];
for(let mask=0;mask<2**R;mask++){
  let positive=0;
  for(let r=0;r<R;r++)positive+=(mask>>r)&1;
  rows.push({mask,positive_repositories:positive,issue_level_p:pval(M*positive,M*(R-positive)),repository_level_p:pval(positive,R-positive)});
}
const naive=rows.filter(r=>r.issue_level_p<=alpha).length;
const clustered=rows.filter(r=>r.repository_level_p<=alpha).length;
if(naive!==12 || clustered!==0 || rows.length!==32)throw Error("unexpected enumeration");
console.log(JSON.stringify({design:{repositories:R,issues_per_repository:M,perfect_within_repo_dependence:true,null:"independent fair repository signs",alpha},assignments:rows.length,issue_level_false_rejections:naive,issue_level_type1_error:naive/rows.length,repository_level_false_rejections:clustered,repository_level_type1_error:clustered/rows.length,rows},null,2));
