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

        if(c_score>o_score):
            curteam.points+=3
        elif(o_score>c_score):
            oppteam.points+=3
        else:
            curteam.points+=1
            oppteam.points+=1

    def run_simulation(self):
        for c in self.teamdetails:
            for o in self.teamdetails:
                if(c!=o):
                    self.play_match(c,o)
                    
    def get_html_report(self):
        # Convert OOP data to Pandas
        data = [{"Rank": 0, "Team": t.tname, "Points": t.points, "GoalsFor": t.gfor, "GoalsAgainst": t.gagainst, "GoalDifferencce": t.gfor-t.gagainst} for t in self.teamdetails]
        df = pd.DataFrame(data)
        df=df.sort_values(by="Points", ascending=False)
        df["Rank"] = range(1, len(df) + 1) 

        table_html = df.to_html(index=False)
        table_html = table_html.replace('<tr>','<tr class="winner">',1)
        return table_html

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

table=obj.get_html_report()

with open("display.html","r",encoding="utf-8") as f:
    html_template=f.read()

final_html = html_template.replace("{{TABLE}}",table)
with open("finaldisplay.html", "w", encoding="utf-8") as f:
    f.write(final_html)
print("\nSimulation Complete!")
print("Opening dispalyresult.html in browser...")

webbrowser.open(
    'file://' + os.path.realpath("finaldisplay.html")
)

    



            



