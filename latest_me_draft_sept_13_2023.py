import numpy as np
import math
import matplotlib.pyplot as plt


def mecalc(meso,bags,skill_level,target_hp,printbool=False):
    
    # Damage calc involving mesos dropped
    if meso <=1000:
        ratio=(meso*0.82+28)/5300
    else:
        ratio=meso/(meso+5250)
        
    skill_data=np.array([500,520,540,560,580,600,620,640,660,680,700,720,740,\
                         760,780,760,779,798,817,836,765,782,790,799,807,720,\
                             727,735,742,750])

    
    # How many bags consumed per click & how many hits per click
    if skill_level <6:
        consume=10
        hits=10
    elif skill_level >5 and skill_level <11:
        consume=12
        hits=12
    elif skill_level >10 and skill_level <16:
        consume=14
        hits=14
    elif skill_level >15 and skill_level <21:
        consume=16
        hits=15
    elif skill_level >20 and skill_level <26:
        consume=18
        hits=15
    elif skill_level >25:
        consume=20
        hits=15
    
    
    # Damage calc estimate, for one hit
    min_dmg=int(50*skill_data[skill_level-1]*0.5*ratio)
    max_dmg=min_dmg*2
    avg_dmg=int((min_dmg+max_dmg)/2)
    
    
    # Total damage, for one click
    if bags<15:
        hits=bags
        
    oneclick_min=min_dmg*hits
    oneclick_max=max_dmg*hits
    oneclick_avg=int((oneclick_min+oneclick_max)/2)
    
    
    # Considering all bags
    clicks=bags/consume
    if clicks % 1 != 0:
        all_min=int(min_dmg*int(clicks)*hits+min_dmg*(bags-int(clicks)*consume))
        all_max=int(max_dmg*int(clicks)*hits+max_dmg*(bags-int(clicks)*consume))
    else:
        all_min=int(min_dmg*clicks*hits)
        all_max=int(max_dmg*clicks*hits)
    
    all_avg=int((all_min+all_max)/2)
    kill_chance=(all_max-target_hp+1)/(all_max-all_min+1)*100 # ints you want / Possible damage ints
    

    # Damage per bag
    if printbool==True:
        print("\nFor 1 line:")
        print("Min dmg:",min_dmg)
        print("Max dmg:",max_dmg)
        print("Avg dmg:",avg_dmg)
        
        print("\nFor 1 click, with [",hits,"] lines:")
        print("Min total:",oneclick_min)
        print("Max total:",oneclick_max)
        print("Avg total:",oneclick_avg)
        
        print("\nFor all [",bags,"] bags:")
        print("Meso per bag:",meso)
        print("Total mesos spent:",meso*bags)
        print("ALL min: ",all_min)
        print("ALL max: ",all_max)
        print("ALL avg: ",all_avg)
        
        print("\n% to kill:",np.round(kill_chance,2))
    
    if printbool==False:
        return(all_min)
    else:
        return("")
        


"""
# Bag constant
all_min=0
while all_min<target_hp and bags<=bags_max and meso<=meso_max:
    all_min=mecalc(meso,bags,skill_level,target_hp)
    meso+=meso_sampl
    
    if meso>=meso_max and all_min<target_hp:
        bags+=bags_sampl
        meso=10
    
print("Target HP:",target_hp,"\n"\
      "All min. damage:",all_min,"\n"\
      "Meso/bag:",meso-meso_sampl,"\n"\
      "# of bags:",bags,"\n")
"""



def dmg_loop(target_hp,skill_level=20):
    
    meso=100
    bags=1
    meso_max=7000
    meso_sampl=10
    bags_max=32
    bags_sampl=1
    
    meso_arr=np.arange(meso,meso_max+meso_sampl,meso_sampl)
    bags_arr=np.zeros(np.size(meso_arr))


    # Meso constant
    i=0
    while i<np.size(meso_arr):
        all_min=0
        bags=1 # INITIALIZE
        
        while all_min<target_hp and bags<=bags_max and meso<=meso_max:
            all_min=mecalc(meso_arr[i],bags,skill_level,target_hp)
            bags+=bags_sampl
            
            if bags>=bags_max and all_min<target_hp:
                meso+=meso_sampl
                bags=1
                i+=1
        
        if all_min>=target_hp:
            if bags>0:
                bags_arr[i]=bags-bags_sampl
            else:
                bags_arr[i]=bags
                
        i+=1
    
    
    """
    # Bag constant
    bags_arr=np.arange(bags,bags_max+bags_sampl,bags_sampl)
    meso_arr=np.zeros(np.size(bags_arr))

    i=0
    while i<np.size(bags_arr):
        all_min=0
        meso=1000 # INITIALIZE
        
        while all_min<target_hp and bags<=bags_max and meso<=meso_max:
            all_min=mecalc(meso,bags_arr[i],skill_level,target_hp)
            meso+=meso_sampl
            
            if meso>=meso_max and all_min<target_hp:
                meso+=meso_sampl
                bags=1
                i+=1
        
        if all_min>=target_hp:
            if bags>0:
                bags_arr[i]=bags-bags_sampl
            else:
                bags_arr[i]=bags
                
        i+=1
    """
    
    
    return(meso_arr,bags_arr,skill_level)



def table(target_hp,sort_type="cost",skill_level=20):
    
    meso,bags,skill_level=dmg_loop(target_hp,skill_level)
    all_min=np.zeros(np.size(meso))
    cost=np.zeros(np.size(meso))
    
    for i in range(0,np.size(meso)):
        all_min[i]=mecalc(meso[i],bags[i],skill_level=skill_level,\
                          target_hp=target_hp)
        cost[i]=meso[i]*bags[i]
    
    
    # Remove rows of 0
    for i in cost:
        if i==0:
            loc=np.where(cost==0)[0][0]
            meso=np.delete(meso,loc)
            bags=np.delete(bags,loc)
            all_min=np.delete(all_min,loc)
            cost=np.delete(cost,loc)
    
    
    # Sort rows in ascending sort_type
    if sort_type!="meso":
        _meso=np.zeros(np.size(meso))
        _bags=np.zeros(np.size(bags))
        _all_min=np.zeros(np.size(all_min))
        _cost=np.zeros(np.size(cost))
        
    else:
        _meso=meso
        _bags=bags
        _all_min=all_min
        _cost=cost
        
    
    j=0
    if sort_type=="bags":
        for i in bags:
            loc=np.where(bags==np.min(bags))[0][0]
            
            _meso[j]=meso[loc]
            _bags[j]=bags[loc]
            _all_min[j]=all_min[loc]
            _cost[j]=cost[loc]
            
            meso=np.delete(meso,loc)
            bags=np.delete(bags,loc)
            all_min=np.delete(all_min,loc)
            cost=np.delete(cost,loc)
            
            j+=1
            
    elif sort_type=="all_min":
        for i in cost:
            loc=np.where(all_min==np.min(all_min))[0][0]
            
            _meso[j]=meso[loc]
            _bags[j]=bags[loc]
            _all_min[j]=all_min[loc]
            _cost[j]=cost[loc]
            
            meso=np.delete(meso,loc)
            bags=np.delete(bags,loc)
            all_min=np.delete(all_min,loc)
            cost=np.delete(cost,loc)
            
            j+=1
            
    elif sort_type=="cost":
        for i in cost:
            loc=np.where(cost==np.min(cost))[0][0]
            
            _meso[j]=meso[loc]
            _bags[j]=bags[loc]
            _all_min[j]=all_min[loc]
            _cost[j]=cost[loc]
            
            meso=np.delete(meso,loc)
            bags=np.delete(bags,loc)
            all_min=np.delete(all_min,loc)
            cost=np.delete(cost,loc)
            
            j+=1

    
    table_arr=np.array((_meso,_bags,_all_min,_cost))
    table_arr=table_arr.T


    return(table_arr)



def dpm(target_hp,skill_level=20):
    # ME animation, 23,17,16 frames // 23
    # total time limit = number of rounds * (time/consumption + recharge)
    
    if skill_level <6:
        consume=10
    elif skill_level >5 and skill_level <11:
        consume=12
    elif skill_level >10 and skill_level <16:
        consume=14
    elif skill_level >15 and skill_level <21:
        consume=16
    elif skill_level >20 and skill_level <26:
        consume=18
    elif skill_level >25:
        consume=20
    
    meso=1000
    bags=400
    recharge=3*60 # 3min
    time=60*60
    _time=60*60
    fps=23/60 # Frames per click
    
    clicks=bags/consume # Total clicks
    clicks=math.ceil(clicks)
    click_time=clicks*fps
    
    all_min=0
    while time>0:
        all_min+=mecalc(meso,bags,skill_level,target_hp)

        time-=click_time
        if time>recharge+click_time: # Still have enough time to fully bomb
            time-=recharge
        else:
            break
    
    print("meLv:",skill_level,"total time [min.]: ",(_time-time)/60)
    
    
    return(all_min,_time)



def plotter(target_hp,plot_type="bags",meso=1000):
    
    # Cost vs. bags
    if plot_type=="bags":
        table_arr=table(target_hp)
        meso=table_arr[:,0]
        bags=table_arr[:,1]
        all_min=table_arr[:,2]
        cost=table_arr[:,3]
        
        x,y=bags,cost
        f,ax=plt.subplots()
        ax.scatter(x,y)
        plt.xlabel("Bags")
        plt.ylabel("Cost")
        plt.title("Mob HP: %(target_hp)s" % {"target_hp":target_hp})
        ax.grid(True)
        ax.minorticks_on()
        
        
    # Cost vs. meso
    if plot_type=="meso":
        table_arr=table(target_hp)
        meso=table_arr[:,0]
        bags=table_arr[:,1]
        all_min=table_arr[:,2]
        cost=table_arr[:,3]
        
        x,y=meso,cost
        f,ax=plt.subplots()
        ax.scatter(x,y)
        plt.xlabel("Meso")
        plt.ylabel("Cost")
        plt.title("Mob HP: %(target_hp)s" % {"target_hp":target_hp})
        ax.grid(True)
        ax.minorticks_on()
        
        
    # Cost vs. skill_level
    elif plot_type=="skill_level":
        skill_level=np.arange(1,30+1,1)
        cost=np.zeros(np.size(skill_level))
        
        j=0
        for i in skill_level:
            table_arr=table(target_hp,"cost",i)
            cost[j]=table_arr[:,3][0]
            
            j+=1
        
        x,y=skill_level,cost
        f,ax=plt.subplots()
        ax.plot(skill_level,cost)
        plt.xlabel("Skill level")
        plt.ylabel("Cost")
        plt.title("Mob HP:%(target_hp)s" %\
                  {"target_hp":target_hp})
        ax.grid(True)
        ax.minorticks_on()
            
            
    # all_min vs. skill_level (DPS: one-full-consumption)
    elif plot_type=="dps":
    
        # A common multiple between 16 and 20 is 400
        # 25 clicks for lvl 20 to bomb 400
        # 20 clicks for lvl 30 to bomb 400
        # mecalc(1000,20*16,20,1.7e6,True) -> all_min: 1003200
        # mecalc(1000,20*20,30,1.7e6,True) -> all_min:  900000
        #
        # LCM of all levels is 5040. Lowest # of clicks to reach is 252,
        #   for levels 26+
        # We will investigate how much dmg. each lvl will deal, for 252 clicks
        
        consume=np.arange(10,22,2)
        lcm=1
        
        for i in range(0,np.size(consume)-1):
            lcm=np.lcm(lcm,consume[i])
            lcm=np.lcm(lcm,consume[i+1])
        
        skill_level=np.arange(1,30+1,1)
        all_min=np.zeros(np.size(skill_level))
        
        for i in range(1,31,1):
            
            if i <6:
                consume=10
            elif i >5 and i <11:
                consume=12
            elif i >10 and i <16:
                consume=14
            elif i >15 and i <21:
                consume=16
            elif i >20 and i <26:
                consume=18
            elif i >25:
                consume=20
            
            all_min[i-1]=mecalc(meso,consume,i,target_hp,False)
        
        
        x,y=skill_level,all_min
        f,ax=plt.subplots()
        ax.plot(x,y)
        plt.xlabel("Skill level")
        plt.ylabel("Min dmg.")
        plt.title("One Full-bag consumption // Meso: %(meso)s" %\
                  {"meso":meso})
        ax.grid(True)
        ax.minorticks_on()

            
    # all_min vs. skill_level (DPM: Considering a time interval)
    elif plot_type=="dpm":
        
        skill_level=np.arange(1,30+1,1)
        all_min=np.zeros(np.size(skill_level))
        
        for i in skill_level:
            _all_min,time=dpm(target_hp,i)
            all_min[i-1]=_all_min
        
        
        x,y=skill_level,all_min
        f,ax=plt.subplots()
        ax.plot(x,y)
        plt.xlabel("Skill level")
        plt.ylabel("Min dmg.")
        plt.title("Time [min.]: %(time)s // Meso: %(meso)s" %\
                  {"time":time/60,"meso":meso})
        ax.grid(True)
        ax.minorticks_on()
        
    
    return(x,y)
            


bub=table(5.1e4,"cost")
bub=plotter((1.7e6),"dpm") # str_kwargs: bags, meso, skill_level, dps, dpm
#for i in range(1,31):
#    bub=dpm(1.7e6,i)

















