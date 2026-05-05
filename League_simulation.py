import numpy as np
import pandas as pd
import webbrowser
import os

class Team_data:
    def __init__(self,tname,tar,tdr):# tar-team attack rate , tdr-team defence rate
        self.tname=tname
        self.tar=tar
        self.tdr=tdr
        self.points=0
        self.gfor=0
        self.gagainst=0
        self.wins = 0
        self.losses=0
        self.draws = 0
        self.win_probability = 0.0

class League_simulation:
    def __init__(self,team_details):
        self.teamdetails=team_details
        self.results=[]

    def play_match(self,curteam,oppteam):
        c_team_lambda=curteam.tar/oppteam.tdr
        o_team_lambda=oppteam.tar/curteam.tdr

        c_score=np.random.poisson(max(0.1,c_team_lambda))
        o_score=np.random.poisson(max(0.1,o_team_lambda))

        curteam.gfor+=c_score
        curteam.gagainst+=o_score
        oppteam.gfor+=o_score
        oppteam.gagainst+=c_score

#changes made to accomodate result match for Award comp

        if(c_score>o_score):
            curteam.points+=3
            curteam.wins+=1
            oppteam.losses+=1
        elif(o_score>c_score):
            oppteam.points+=3
            curteam.losses+=1
            oppteam.wins+=1
        else:
            curteam.points+=1
            oppteam.points+=1
            curteam.draws+=1
            oppteam.draws+=1

        #logging indv. match result
        self.results.append({
            "Home"    : curteam.tname,
            "Away"    : oppteam.tname,
            "Home GF" : c_score,
            "Away GF" : o_score,
        })

    def run_simulation(self):
        for c in self.teamdetails:
            for o in self.teamdetails:
                if(c!=o):
                    self.play_match(c,o)

#new fucntion to analyze best performer
    def get_awards(self):
        
        top_team     = max(self.teamdetails, key=lambda t: t.points)
        best_attack  = max(self.teamdetails, key=lambda t: t.gfor)
        best_defence = min(self.teamdetails, key=lambda t: t.gagainst)
        return top_team, best_attack, best_defence



    def get_html_report(self):
        # Convert OOP data to Pandas
        data = [{"Rank": 0, 
                 "Team": t.tname, 
                 "Matches Played": t.wins+t.draws+t.losses,
                 "W"  : t.wins,
                 "D": t.draws,
                 "L":t.losses,  #changes were made here for W/D/L/MP
                 "Points": t.points, 
                 "GoalsFor": t.gfor, 
                 "GoalsAgainst": t.gagainst, 
                 "GoalDifference": abs(t.gfor-t.gagainst)} for t in self.teamdetails]
        
        df = pd.DataFrame(data)
        df=df.sort_values(by="Points", ascending=False)
        df["Rank"] = range(1, len(df) + 1) 

        table_html = df.to_html(index=False)
        table_html = table_html.replace('<tr>','<tr class="winner">',1)
        return table_html
    
    def get_awards_table_html(self):
        awards = self.get_awards()

        award_data = [
            {
                "Award": "🏆 Top Team",
                "Winner": awards[0].tname,
                "Stat": str(awards[0].points) + " pts"
            },
            {
                "Award": "⚡ Best Attack",
                "Winner": awards[1].tname,
                "Stat": str(awards[1].gfor) + " goals"
            },
            {
                "Award": "🛡 Best Defence",
                "Winner": awards[2].tname,
                "Stat": str(awards[2].gagainst) + " conceded"
            }
        ]

        df = pd.DataFrame(award_data)
        return df.to_html(index=False)
    

    def get_mc_html(self):
        mc_data = [{
            "Team"               : t.tname,
            "Win Probability %"  : t.win_probability,
            "Loss Probability %"  : round(100 - t.win_probability, 1)
        } for t in self.teamdetails]
        
        mc_df = pd.DataFrame(mc_data).sort_values("Win Probability %", ascending=False)
        return mc_df.to_html(index=False)

    
    def run_monte_carlo(self, trials=5000):
        for a in self.teamdetails:
            for b in self.teamdetails:
                if a == b:
                    continue
                wins = 0
                for _ in range(trials):
                    ga = np.random.poisson(max(0.1, a.tar / b.tdr))
                    gb = np.random.poisson(max(0.1, b.tar / a.tdr))
                    if ga > gb:
                        wins += 1
                a.win_probability += round(wins / trials * 100, 1)

print("Ready to Simulate League?")
num=int(input("Enter number of Teams:")) 
details=[]

for i in range(num):
    name=input("Enter Team name:")
    offrate=float(input("Enter offense rate of the Team : "))
    defrate=float(input("Enter the Defense rate of the Team : "))
    details.append(Team_data(name,offrate,defrate))
obj=League_simulation(details)    
obj.run_simulation()


awards_html = obj.get_awards_table_html()

obj.run_monte_carlo()
mc_html = obj.get_mc_html()
table=obj.get_html_report()

with open("display.html","r",encoding="utf-8") as f:
    html_template=f.read()

final_html = html_template.replace("{{TABLE}}",table)
final_html = final_html.replace("{{AWARDS}}",awards_html)
final_html = final_html.replace("{{MC_TABLE}}", mc_html)

with open("finaldisplay.html", "w", encoding="utf-8") as f:
    f.write(final_html)
print("\nSimulation Complete!")
print("Opening dispalyresult.html in browser...")




webbrowser.open(
    'file://' + os.path.realpath("finaldisplay.html")
)

    



""" 1, Typo fix
2, Result=[] sub-used for total match storage and review
3, W/D/L track -> three awards pos
4, Comment for logic 
5, total matches played"""

""" Changes in CSS and HTML + Display logic list usuage at result = []"""

