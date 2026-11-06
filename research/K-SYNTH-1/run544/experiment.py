import itertools, math, json
def exact_p(d, groups):
    observed=abs(sum(d))
    return sum(abs(sum(sign*sum(d[i] for i in group) for sign,group in zip(signs,groups)))>=observed for signs in itertools.product((-1,1),repeat=len(groups)))/2**len(groups)
def test():
    rows=[]
    for k in range(1,9):
        d=[1]*(4*k)+[-1]*(4*(8-k))
        groups=[list(range(4*j,4*j+4)) for j in range(8)]
        obs=abs(sum(d))
        naive=sum(math.comb(32,j) for j in range(33) if abs(2*j-32)>=obs)/2**32
        rows.append(dict(positive_repos=k,negative_repos=8-k,observed_margin=sum(d),naive_p=naive,cluster_p=exact_p(d,groups)))
    assert rows[6]['naive_p']<.05<rows[6]['cluster_p']
    assert rows[7]['cluster_p']==2/256
    for mult in (1,2,4,10):
        d=[1]*(7*mult)+[-1]*mult
        groups=[list(range(i*mult,(i+1)*mult)) for i in range(8)]
        assert exact_p(d,groups)==rows[6]['cluster_p']
    return dict(rows=rows,assertions=4,scope='synthetic exact sign-flip illustration; not empirical model evidence')
if __name__=='__main__':print(json.dumps(test(),indent=2))
