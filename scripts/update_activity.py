"""Generate a contribution calendar from GitHub GraphQL data, using only stdlib."""
from datetime import date, datetime, timezone
from html import escape
import json, os, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEST = ROOT / 'assets' / 'activity.svg'
QUERY = '''query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date weekday contributionCount } }
      }
    }
  }
}'''
COLORS = ['#25191c', '#53282e', '#824047', '#ac5d61', '#e39b94']

def fetch():
    req = urllib.request.Request('https://api.github.com/graphql',
        data=json.dumps({'query':QUERY,'variables':{'login':os.environ['PROFILE_LOGIN']}}).encode(),
        headers={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'], 'Content-Type':'application/json','User-Agent':'b-positive-profile'},method='POST')
    with urllib.request.urlopen(req, timeout=40) as resp:
        obj=json.load(resp)
    if obj.get('errors'):
        raise RuntimeError('GitHub GraphQL: '+str(obj['errors']))
    return obj['data']['user']['contributionsCollection']['contributionCalendar']

def render(cal, today=None):
    weeks=cal['weeks']; total=cal['totalContributions']
    if not weeks or len(weeks)>54: raise ValueError('Unexpected calendar size')
    peak=max((day['contributionCount'] for week in weeks for day in week['contributionDays']),default=0)
    stamp=(today or datetime.now(timezone.utc).date()).isoformat()
    s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 250" role="img" aria-labelledby="title desc">',
       '<title id="title">Noospheric activity</title>',f'<desc id="desc">{total} contributions in the GitHub calendar. Updated {stamp} UTC.</desc>',
       '<rect x="1" y="1" width="958" height="248" rx="10" fill="#101013" stroke="#553437" stroke-width="2"/>',
       '<g font-family="monospace" font-size="15">',
       '<text x="22" y="31" fill="#c67b7c" font-weight="bold">NOOSPHERIC ACTIVITY // CONTRIBUTION ARCHIVE</text>',
       f'<text x="938" y="31" text-anchor="end" fill="#aaa09a" font-size="13">UPDATED {stamp} UTC</text>',
       '<path d="M22 44H938" stroke="#553437"/>']
    step=min(16, 875/len(weeks)); x0=60; y0=78
    month=None
    for i,week in enumerate(weeks):
        for day in week['contributionDays']:
            dt=date.fromisoformat(day['date']); n=day['contributionCount']; wd=day['weekday']; x=x0+i*step; y=y0+wd*16
            level=0 if n==0 else min(4,1+int(3*n/max(1,peak)))
            s.append(f'<rect x="{x:.2f}" y="{y}" width="{step-3:.2f}" height="13" rx="2" fill="{COLORS[level]}"><title>{dt}: {n} contributions</title></rect>')
        if week['contributionDays']:
            dt=date.fromisoformat(week['contributionDays'][0]['date'])
            if dt.month!=month:
                month=dt.month
                if i==0 or i>=2: s.append(f'<text x="{x0+i*step:.2f}" y="67" fill="#aaa09a" font-size="11">{dt.strftime("%b")}</text>')
    for label,wd in [('Mon',1),('Wed',3),('Fri',5)]: s.append(f'<text x="22" y="{y0+wd*16+10}" fill="#aaa09a" font-size="11">{label}</text>')
    s.append('<rect x="60" y="78" width="2" height="109" fill="#e39b94" opacity="0.55"><animate attributeName="x" from="60" to="933" dur="9s" repeatCount="indefinite"/></rect>')
    s.extend(['<path d="M22 199H938" stroke="#553437"/>', f'<text x="22" y="226" fill="#eee3d5">{total} contributions</text>', '<text x="938" y="226" text-anchor="end" fill="#aaa09a" font-size="12">LESS  /  MORE ACTIVITY</text>'])
    for i,c in enumerate(COLORS): s.append(f'<rect x="{679+i*19}" y="214" width="15" height="15" rx="2" fill="{c}"/>')
    s.append('</g></svg>')
    return '\n'.join(s)+'\n'

if __name__=='__main__':
    svg=render(fetch())
    tmp=DEST.with_suffix('.tmp');tmp.write_text(svg,encoding='utf-8');tmp.replace(DEST)
