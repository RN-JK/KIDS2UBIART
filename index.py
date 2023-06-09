import os, struct, json, shutil, random
import numpy as np
#from unidecode import unidecode

#functions
def hex_to_rgb(value): 
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def ubiarttime(time): #credits to planedec for this script to make synced times for ubiart
    return int(np.interp(time+48,beats,beatindexes)-2)

def removeduplicate(it):
    seen = []
    for x in it:
        if x not in seen:
            yield x
            seen.append(x)

def readLogs():
    print('Moves0: '+str(len(moves0)))
    print('Moves1: '+str(len(moves1)))
    print('Beats: '+str(len(beats)))
    print('Pictos: '+str(len(pictos)))
    print('Lyrics: '+str(len(lyrics)))
    print('GoldEffects: '+str(len(goldmoves)))
    print('HideUserInterface: '+str(len(hideui)))
    print('Shake Moves: '+str(len(shakemoves)))
    input()

class UbiArt:
    def Tape(tape, mapName):
        tape['__class']='Tape'
        tape['Clips']=[]
        tape['TapeClock']=0
        tape['TapeBarCount']=1
        tape['FreeResourcesAfterPlay']=0
        tape['MapName']=mapName
        tape['SoundwichEvent']=""

    def TPL(tpl):
        tpl['__class']='Actor_Template'
        tpl['WIP']=0
        tpl['LOWUPDATE']=0
        tpl['UPDATE_LAYER']=0
        tpl['PROCEDURAL']=0
        tpl['STARTPAUSED']=0
        tpl['FORCEISENVIRONMENT']=0
        tpl['COMPONENTS']=[]

    def genericClip(clip, classname, array):
        clip['__class']=classname
        clip['Id']=random.randint(10000000, 99999999)
        clip['TrackId']=random.randint(10000000, 99999999)
        clip['IsActive']=1
        clip['StartTime']=ubiarttime(array['time'])
        clip['Duration']=ubiarttime(array['duration'])

    def convert2UbiArt():
        #songdesc
        songdesctpl={}
        UbiArt.TPL(songdesctpl)
        songdesctemplate={}
        songdesctemplate["__class"]="JD_SongDescTemplate"
        songdesctemplate["MapName"]=mapname
        songdesctemplate["JDVersion"]=2016
        songdesctemplate["OriginalJDVersion"]=setting['originalJDVersion']
        songdesctemplate["Artist"]=setting["artist"]
        songdesctemplate["DancerName"]="Unknown Dancer"
        songdesctemplate["Title"]=setting["title"]
        songdesctemplate["NumCoach"]=setting["numCoach"]
        songdesctemplate["MainCoach"]=-1
        songdesctemplate["Difficulty"]=setting['difficulty']
        songdesctemplate["SweatDifficulty"]=setting['sweatDifficulty']
        songdesctemplate["backgroundType"]=0
        songdesctemplate["LyricsType"]=0
        songdesctemplate["Energy"]=1
        songdesctemplate["Tags"]=["main"]
        songdesctemplate["Status"]=3
        songdesctemplate["LocaleID"]=4294967295
        songdesctemplate["MojoValue"]=0
        songdesctemplate["CountInProgression"]=1
        defaultcolors={}
        defaultcolors["lyrics"]=[hex_to_rgb(lyriccolor)[0]/255,hex_to_rgb(lyriccolor)[1]/255,hex_to_rgb(lyriccolor)[2]/255,hex_to_rgb(lyriccolor)[3]/255]
        defaultcolors["theme"]=[1,1,1,1]
        songdesctemplate["DefaultColors"]=defaultcolors
        songdesctemplate["VideoPreviewPath"]=""
        songdesctpl['COMPONENTS'].append(songdesctemplate)
        json.dump(songdesctpl,open('output/'+mapname+'/songdesc.tpl.ckd','w'))

        #musictrack
        musictracktpl={}
        UbiArt.TPL(musictracktpl)
        trackdata={"__class": "MusicTrackComponent_Template", "trackData": {"__class": "MusicTrackData", "structure": {"__class": "MusicTrackStructure", "markers": [], "signatures": [{"__class": "MusicSignature", "marker": 0, "beats": 4}], "sections": [{"__class": "MusicSection", "marker": 16, "sectionType": 8, "comment": ""}], "startBeat": 0, "endBeat": len(beats), "fadeStartBeat": 0, "useFadeStartBeat": False, "fadeEndBeat": 0, "useFadeEndBeat": False, "videoStartTime": 0, "previewEntry": round(len(beats)/4), "previewLoopStart": round(len(beats)/3), "previewLoopEnd": round(len(beats)/2), "volume": 0, "fadeInDuration": 0, "fadeInType": 0, "fadeOutDuration": 0, "fadeOutType": 0}, "path": "world/maps/"+mapname.lower()+"/audio/"+mapname.lower()+".wav", "url": "jmcs://jd-contents/"+mapname+"/"+mapname+".ogg"}}

        for beat in beats:
            trackdata['trackData']['structure']['markers'].append(beat*48)

        musictracktpl['COMPONENTS'].append(trackdata)
        json.dump(musictracktpl,open('output/'+mapname+'/'+mapname.lower()+'_musictrack.tpl.ckd','w'))
        
        #dtape
        dtape={}
        UbiArt.Tape(dtape, mapname)

        #moves0
        for move in moves0:
            MotionClip={}
            UbiArt.genericClip(MotionClip, 'MotionClip', move)
            MotionClip['StartTime']=MotionClip['StartTime']+setting['offset']['moves']
            MotionClip['ClassifierPath']="world/maps/"+mapname.lower()+"/timeline/moves/"+move['name']+'.msm'
            try:
                MotionClip['GoldMove']=move['goldMove']
            except:
                MotionClip['GoldMove']=0
            MotionClip['MoveType']=0
            MotionClip['CoachId']=0
            MotionClip['Color']=[1,1,1,1]
            MotionClip['MotionPlatformSpecifics']={
				"X360": {
					"__class": "MotionPlatformSpecific",
					"ScoreScale": 1,
					"ScoreSmoothing": 0,
					"ScoringMode": 0
				},
				"ORBIS": {
					"__class": "MotionPlatformSpecific",
					"ScoreScale": 1,
					"ScoreSmoothing": 0,
					"ScoringMode": 0
				},
				"DURANGO": {
					"__class": "MotionPlatformSpecific",
					"ScoreScale": 1,
					"ScoreSmoothing": 0,
					"ScoringMode": 0
				}
			}

            dtape['Clips'].append(MotionClip)

        #moves1
        for move in moves1:
            MotionClip={}
            UbiArt.genericClip(MotionClip, 'MotionClip', move)
            MotionClip['StartTime']=MotionClip['StartTime']+setting['offset']['moves']
            MotionClip['ClassifierPath']="world/maps/"+mapname.lower()+"/timeline/moves/"+move['name']+'.msm'
            try:
                MotionClip['GoldMove']=move['goldMove']
            except:
                MotionClip['GoldMove']=0
            MotionClip['MoveType']=0
            MotionClip['CoachId']=1
            MotionClip['Color']=[1,1,1,1]
            MotionClip['MotionPlatformSpecifics']={
				"X360": {
					"__class": "MotionPlatformSpecific",
					"ScoreScale": 1,
					"ScoreSmoothing": 0,
					"ScoringMode": 0
				},
				"ORBIS": {
					"__class": "MotionPlatformSpecific",
					"ScoreScale": 1,
					"ScoreSmoothing": 0,
					"ScoringMode": 0
				},
				"DURANGO": {
					"__class": "MotionPlatformSpecific",
					"ScoreScale": 1,
					"ScoreSmoothing": 0,
					"ScoringMode": 0
				}
			}

            dtape['Clips'].append(MotionClip)

        #kinect_moves0
        for move in kinect_moves0:
            MotionClip={}
            UbiArt.genericClip(MotionClip, 'MotionClip', move)
            MotionClip['StartTime']=MotionClip['StartTime']+setting['offset']['moves']
            MotionClip['ClassifierPath']="world/maps/"+mapname.lower()+"/timeline/moves/"+move['name']+'.gesture'
            try:
                MotionClip['GoldMove']=move['goldMove']
            except:
                MotionClip['GoldMove']=0
            MotionClip['MoveType']=1
            MotionClip['CoachId']=0
            MotionClip['Color']=[1,1,1,1]
            MotionClip['MotionPlatformSpecifics']={
				"X360": {
					"__class": "MotionPlatformSpecific",
					"ScoreScale": 1,
					"ScoreSmoothing": 0,
					"ScoringMode": 0
				},
				"ORBIS": {
					"__class": "MotionPlatformSpecific",
					"ScoreScale": 1,
					"ScoreSmoothing": 0,
					"ScoringMode": 0
				},
				"DURANGO": {
					"__class": "MotionPlatformSpecific",
					"ScoreScale": 1,
					"ScoreSmoothing": 0,
					"ScoringMode": 0
				}
			}

            dtape['Clips'].append(MotionClip)

        #kinect_moves1
        for move in kinect_moves1:
            MotionClip={}
            UbiArt.genericClip(MotionClip, 'MotionClip', move)
            MotionClip['StartTime']=MotionClip['StartTime']+setting['offset']['moves']
            MotionClip['ClassifierPath']="world/maps/"+mapname.lower()+"/timeline/moves/"+move['name']+'.gesture'
            try:
                MotionClip['GoldMove']=move['goldMove']
            except:
                MotionClip['GoldMove']=0
            MotionClip['MoveType']=1
            MotionClip['CoachId']=1
            MotionClip['Color']=[1,1,1,1]
            MotionClip['MotionPlatformSpecifics']={
				"X360": {
					"__class": "MotionPlatformSpecific",
					"ScoreScale": 1,
					"ScoreSmoothing": 0,
					"ScoringMode": 0
				},
				"ORBIS": {
					"__class": "MotionPlatformSpecific",
					"ScoreScale": 1,
					"ScoreSmoothing": 0,
					"ScoringMode": 0
				},
				"DURANGO": {
					"__class": "MotionPlatformSpecific",
					"ScoreScale": 1,
					"ScoreSmoothing": 0,
					"ScoringMode": 0
				}
			}

            dtape['Clips'].append(MotionClip)

        #spltting shake move clips
        if setting['shakeRange']==0:
            pass
        else:
            for move in shakemoves:
                starttime=ubiarttime(move['time'])
                duration=ubiarttime(move['duration'])
                endtime=starttime+duration
                for time in range(starttime,endtime, setting['shakeRange']):
                    MotionClip={}
                    UbiArt.genericClip(MotionClip, 'MotionClip', move)
                    MotionClip['StartTime']=time+setting['offset']['moves']
                    MotionClip['Duration']=setting['shakeRange']
                    MotionClip['ClassifierPath']="world/maps/"+mapname.lower()+"/timeline/moves/"+move['name']+'.msm'
                    try:
                        MotionClip['GoldMove']=move['goldMove']
                    except:
                        MotionClip['GoldMove']=0
                    MotionClip['MoveType']=0
                    MotionClip['CoachId']=0
                    MotionClip['Color']=[1,1,1,1]
                    MotionClip['MotionPlatformSpecifics']={
				        "X360": {
					        "__class": "MotionPlatformSpecific",
					        "ScoreScale": 1,
					        "ScoreSmoothing": 0,
					        "ScoringMode": 0
				        },
				        "ORBIS": {
					        "__class": "MotionPlatformSpecific",
					        "ScoreScale": 1,
					        "ScoreSmoothing": 0,
					        "ScoringMode": 0
				        },
				        "DURANGO": {
					        "__class": "MotionPlatformSpecific",
					        "ScoreScale": 1,
					        "ScoreSmoothing": 0,
					        "ScoringMode": 0
				        }
			        }

                    dtape['Clips'].append(MotionClip)

        #pictos
        for picto in pictos:
            PictogramClip={}
            UbiArt.genericClip(PictogramClip, 'PictogramClip', picto)
            PictogramClip['StartTime']=PictogramClip['StartTime']+setting['offset']['pictos']
            PictogramClip['PictoPath']="world/maps/"+mapname.lower()+"/timeline/pictos/"+picto['name']+'.png'
            PictogramClip['MontagePath']=""
            PictogramClip['AtlIndex']=4294967295
            PictogramClip['CoachCount']=4294967295

            dtape['Clips'].append(PictogramClip)

        #goldmoves
        for gold in goldmoves:
            GoldEffectClip={}
            UbiArt.genericClip(GoldEffectClip, 'GoldEffectClip', gold)
            GoldEffectClip['EffectType']=gold['effectType']

            dtape['Clips'].append(GoldEffectClip)


        json.dump(dtape,open('output/'+mapname+'/'+mapname.lower()+'_tml_dance.dtape.ckd','w'))

        #ktape
        ktape={}
        UbiArt.Tape(ktape, mapname)

        for lyric in lyrics:
            KaraokeClip={}
            UbiArt.genericClip(KaraokeClip, 'KaraokeClip', lyric)
            KaraokeClip['StartTime']=KaraokeClip['StartTime']+setting['offset']['lyrics']
            KaraokeClip['Pitch']=261.625549
            KaraokeClip['Lyrics']=lyric['text']
            KaraokeClip['IsEndOfLine']=1
            KaraokeClip['ContentType']=0
            KaraokeClip['StartTimeTolerance']=4
            KaraokeClip['EndTimeTolerance']=4
            KaraokeClip['SemitoneTolerance']=5
            if KaraokeClip['Lyrics']=='\t':
                continue
            elif KaraokeClip['Lyrics']=='!WHITE!' or KaraokeClip['Lyrics']=='!BOARD_ON!' or KaraokeClip['Lyrics']=='!BOARD_OFF!' or KaraokeClip['Lyrics']=='!BLACK!':
                continue
            else:
                ktape['Clips'].append(KaraokeClip)

        json.dump(ktape,open('output/'+mapname+'/'+mapname.lower()+'_tml_karaoke.ktape.ckd','w'))

        #mainsequence
        mainsequence={}
        UbiArt.Tape(mainsequence, mapname)

        if setting['hideuiClips']==True:
            for hui in hideui:
                HideUserInterfaceClip={}
                UbiArt.genericClip(HideUserInterfaceClip, 'HideUserInterfaceClip', hui)
                HideUserInterfaceClip['StartTime']=HideUserInterfaceClip['StartTime']+setting['offset']['hideui']
                HideUserInterfaceClip['EventType']=18
                HideUserInterfaceClip['CustomParam']=""

                if HideUserInterfaceClip['Duration']<=24:
                    continue
                else:
                    mainsequence['Clips'].append(HideUserInterfaceClip)

        #if setting['ambClips']==True:
        #    for amb in ambs:
        #        SoundSetClip={}
        #        UbiArt.genericClip(SoundSetClip, 'SoundSetClip', amb)
        #        SoundSetClip['SoundSetPath']='world/maps/'+mapname.lower()+'/audio/amb/'+amb['name']+'.tpl'
        #        SoundSetClip['SoundChannel']=0
        #        SoundSetClip['StartOffset']=0
        #        SoundSetClip['StopsOnEnd']=0
        #        SoundSetClip['AccountedForDuration']=0

        #        mainsequence['Clips'].append(SoundSetClip)

        json.dump(mainsequence,open('output/'+mapname+'/'+mapname.lower()+'_mainsequence.tape.ckd','w'))


print('''KIDS2UBIART
by: JackLSummer15 & RyanL181095''')
try:
    os.mkdir("input")
    os.mkdir("output")
    print('The directories have been made.')
    input('Insert your files in input and then run the tool again to convert the tapes.')
    exit()

except:
    pass

setting=json.load(open('settings.json'))
mapname=setting['mapName']

lyrics=[]
text=[[],[],[],[],[],[],[],[],[],[],[],[]] #there's multiple brackets because of multiple languages

beats=[]
pictos=[]
moves0=[]
moves1=[]
kinect_moves0=[]
kinect_moves1=[]
shakemoves=[]
goldmoves=[]
hideui=[]
ambs=[]
traces=[]
lyriccolor="FF"+setting['lyrichexColor'].upper().replace('#','')
multiplier=100
mapendtime=0
beatindexes=[]
hideuistarttime=0
hideuiendtime=0
hideuiendduration=0
language=setting['lyricLanguage']

#os.makedirs('output/'+mapname+'/amb', exist_ok=True)
os.makedirs('output/'+mapname+'/gestures_'+setting['gestureType'].lower(), exist_ok=True)
os.makedirs('output/'+mapname+'/moves', exist_ok=True)
os.makedirs('output/'+mapname+'/pictos', exist_ok=True)
count=0
tapeversion=b'\x41\x20\x00\x00'
try:
    dancedata=open('input/'+setting['mapInput']+'_script.bin','rb')
    dancedata.read(4)
    mapendtime=struct.unpack('>f',dancedata.read(4))[0]
    mapendtime=int(mapendtime*1000)
    dancedata.read(4)
    dancecount=struct.unpack('>f',dancedata.read(4))[0]
    tapeversion=dancedata.read(4)
    if tapeversion==b'\x41\xC8\x00\x00' or tapeversion==b'\x40\xC0\x00\x00' or tapeversion==b'\x41\x20\x00\x00': #smurfs, hip hop dance, jdkids 2 & 2014, jddisney 1 & 2
        dancedata.read(24)
    elif tapeversion==b'\x41\xD0\x00\x00': #jdkids 1
        dancedata.read(12)
    for d in range(int(dancecount)):
        classtype=dancedata.read(4)
        if classtype==b'\x41\xC8\x00\x00': #moves
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            gamever=struct.unpack('>f',dancedata.read(4))[0]
            endtime=struct.unpack('>f',dancedata.read(4))[0]
            duration=endtime-starttime
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4) 
            movevalue=struct.unpack('>f',dancedata.read(4))[0]
            dancedata.read(4) 
            goldmove=struct.unpack('>f',dancedata.read(4))[0] #goldmove
            movename=mapname.lower()+'_'+str(int(movevalue))
            shutil.copy('bin/move.msm', 'output/'+mapname+'/moves/'+movename+'.msm')
            move={}
            move['name']=movename
            move['time']=int(starttime*multiplier)
            move['duration']=int(duration*multiplier)
            if int(goldmove)==2:
                move['goldMove']=1

                if setting['goldEffectType']=='move':
                    goldeffect={}
                    goldeffect['time']=int(starttime*multiplier)
                    goldeffect['duration']=1959
                    goldeffect['effectType']=1

                    goldmoves.append(goldeffect)

            if int(gamever)==21 or int(gamever)==8: #jddisney 1 + 2 & jdkids 2014
                #dancedata.read(56)
                coachid=struct.unpack('>f',dancedata.read(4))[0]
                if int(coachid)==3:
                    moves0.append(move)
                elif int(coachid)==5:
                    moves1.append(move)
                elif int(coachid)==7:
                    moves0.append(move)
                    moves1.append(move)
                dancedata.read(52)
            elif int(gamever)==20: #jdkids 2
                moves0.append(move)
                dancedata.read(52)
            elif int(gamever)==9: #smurfs
                moves0.append(move)
                dancedata.read(4)
                dancedata.read(4)
            elif int(gamever)==10: #hiphop dance
                moves0.append(move)
                dancedata.read(12)
            #dancedata.read(24)
        elif classtype==b'\x41\xB0\x00\x00': #moves
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            gamever=struct.unpack('>f',dancedata.read(4))[0]
            endtime=struct.unpack('>f',dancedata.read(4))[0]
            duration=endtime-starttime
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4) 
            movevalue=struct.unpack('>f',dancedata.read(4))[0]
            dancedata.read(4)
            goldmove=struct.unpack('>f',dancedata.read(4))[0]
        
            movename=mapname.lower()+'_'+str(int(movevalue))
            shutil.copy('bin/move.msm', 'output/'+mapname+'/moves/'+movename+'.msm')
            move={}
            move['name']=movename
            move['time']=int(starttime*multiplier)
            move['duration']=int(duration*multiplier)
            if int(goldmove)==2:
                move['goldMove']=1

                if setting['goldEffectType']=='move':
                    goldeffect={}
                    goldeffect['time']=int(starttime*multiplier)
                    goldeffect['duration']=1959
                    goldeffect['effectType']=1

                    goldmoves.append(goldeffect)

            if int(gamever)==7: #jdkids 2
                moves0.append(move)
                #continue
            elif int(gamever)==21 or int(gamever)==8: #jddisney 1 & 2 & jdkids 2014
                #dancedata.read(56)
                coachid=struct.unpack('>f',dancedata.read(4))[0]
                if int(coachid)==3:
                    moves0.append(move)
                elif int(coachid)==5:
                    moves1.append(move)
                elif int(coachid)==7:
                    moves0.append(move)
                    moves1.append(move)
            #dancedata.read(24)
        elif classtype==b'\x41\xA8\x00\x00': #move tapes that makes you not move. (only used in smurfs dance party)
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            gamever=struct.unpack('>f',dancedata.read(4))[0]
            endtime=struct.unpack('>f',dancedata.read(4))[0] 
            duration=endtime-starttime
            unknownvalue=struct.unpack('>f',dancedata.read(4))[0]
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            if int(gamever)==8:
                dancedata.read(8)
            else:
                dancedata.read(4)
            #move={}
            #move['name']="placeholder"
            #move['time']=int(starttime*multiplier)
            #move['duration']=int(duration*multiplier)

            #moves0.append(move)
            #dancedata.read(40)
        elif classtype==b'\x41\xD0\x00\x00': 
            dancedata.read(4)
            if dancedata.read(4)==b'\x3F\x80\x00\x00':
                dancedata.read(4)
        elif classtype==b'\x40\x80\x00\x00': #great... more random classes for basically the same thing..... (jdkids 1 moves)
            endtime=struct.unpack('>f',dancedata.read(4))[0]
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            movevalue=struct.unpack('>f',dancedata.read(4))[0]
            goldmove=struct.unpack('>f',dancedata.read(4))[0]
            duration=endtime-starttime
            movename=mapname.lower()+'_'+str(int(movevalue))
            shutil.copy('bin/move.msm', 'output/'+mapname+'/moves/'+movename+'.msm')
            move={}
            move['name']=movename
            move['time']=int(starttime*multiplier)
            move['duration']=int(duration*multiplier)
            
            if int(goldmove)==2:
                move['goldMove']=1
            if move['time']>=576:
                moves0.append(move)
            #if starttime==2.0 or endtime==1.0:
            #    continue
            #else:
            #    dancedata.read(4)
        elif classtype==b'\x40\xE0\x00\x00': #moves (jdkids 1)
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            hash=dancedata.read(4)
            
            if hash==b'\x00\x00\x00\x00':
                continue
            elif hash==b'\x3E\x19\x99\x9A':
                movevalue=struct.unpack('>f',dancedata.read(4))[0]
                dancedata.read(4)
                goldmove=struct.unpack('>f',dancedata.read(4))[0]
                dancedata.read(4)
                dancedata.read(4)
                dancedata.read(4)
                
                endtime=struct.unpack('>f',dancedata.read(4))[0]
                duration=endtime-starttime
                movename=mapname.lower()+'_'+str(int(movevalue))
                shutil.copy('bin/move.msm', 'output/'+mapname+'/moves/'+movename+'.msm')
                move={}
                move['name']=movename
                move['time']=int(starttime*multiplier)
                move['duration']=int(duration*multiplier)
                if int(goldmove)==2:
                    move['goldMove']=1

                    if setting['goldEffectType']=='move':
                        goldeffect={}
                        goldeffect['time']=int(starttime*multiplier)
                        goldeffect['duration']=1959
                        goldeffect['effectType']=1

                        goldmoves.append(goldeffect)
                moves0.append(move)
            else:
                dancedata.read(4)
                dancedata.read(4)
                dancedata.read(4)
                dancedata.read(4)
                dancedata.read(4)
                dancedata.read(4)
        elif classtype==b'\x40\xC0\x00\x00': #moves (jdkids 1)
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            gamever=struct.unpack('>f',dancedata.read(4))[0]
            if gamever==0.15000000596046448:
                movevalue=struct.unpack('>f',dancedata.read(4))[0]
                dancedata.read(4)
                goldmove=struct.unpack('>f',dancedata.read(4))[0]
                unknownvalue=struct.unpack('>f',dancedata.read(4))[0]
                if not int(unknownvalue)==0 or int(unknownvalue)==4 or not int(unknownvalue)==6:
                    dancedata.read(4)
                    endtime=struct.unpack('>f',dancedata.read(4))[0]
                    duration=endtime-starttime
                    movename=mapname.lower()+'_'+str(int(movevalue))
                    shutil.copy('bin/move.msm', 'output/'+mapname+'/moves/'+movename+'.msm')
                    move={}
                    move['name']=movename
                    move['time']=int(starttime*multiplier)
                    move['duration']=int(duration*multiplier)
                    if int(goldmove)==2:
                        move['goldMove']=1

                        if setting['goldEffectType']=='move':
                            goldeffect={}
                            goldeffect['time']=int(starttime*multiplier)
                            goldeffect['duration']=1959
                            goldeffect['effectType']=1

                            goldmoves.append(goldeffect)
        
                    moves0.append(move)
            elif gamever==0.0 or gamever==1.0 or gamever==79.22000122070312:
                continue
            else:
                dancedata.read(4)
                dancedata.read(4)
                dancedata.read(4)
                dancedata.read(4)
        elif classtype==b'\x40\xA0\x00\x00': #shake moves (jdkids 1)
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            struct.unpack('>f',dancedata.read(4))[0]
            struct.unpack('>f',dancedata.read(4))[0]
            extravalue=struct.unpack('>f',dancedata.read(4))[0]
            goldmove=struct.unpack('>f',dancedata.read(4))[0] #1 = shake move, 2 = gold move
            movevalue=struct.unpack('>f',dancedata.read(4))[0]
            endtime=struct.unpack('>f',dancedata.read(4))[0]
            duration=endtime-starttime
            movename=mapname.lower()+'_'+str(int(movevalue))
            shutil.copy('bin/move.msm', 'output/'+mapname+'/moves/'+movename+'.msm')
            move={}
            move['name']=movename
            move['time']=int(starttime*multiplier)
            move['duration']=int(duration*multiplier)
            if int(goldmove)==1: #shake move
                if int(extravalue)==2:
                    move['goldMove']=1
                shakemoves.append(move)
                #continue
            else:
                if int(goldmove)==2:
                    move['goldMove']=1

                    if setting['goldEffectType']=='move':
                        goldeffect={}
                        goldeffect['time']=int(starttime*multiplier)
                        goldeffect['duration']=1959
                        goldeffect['effectType']=1

                        goldmoves.append(goldeffect)
        
                moves0.append(move)
        elif classtype==b'\x41\xC0\x00\x00':
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            movevalue=struct.unpack('>f',dancedata.read(4))[0]
            
            struct.unpack('>f',dancedata.read(4))[0]
            endtime=struct.unpack('>f',dancedata.read(4))[0]
            duration=endtime-starttime
            struct.unpack('>f',dancedata.read(4))[0]
            if struct.unpack('>f',dancedata.read(4))[0]==1.0:
                dancedata.read(4)
                dancedata.read(4)
            movename=mapname.lower()+'_'+str(int(movevalue))
            shutil.copy('bin/move.msm', 'output/'+mapname+'/moves/'+movename+'.msm')
            move={}
            move['name']=movename
            move['time']=int(starttime*multiplier)
            move['duration']=int(duration*multiplier)
            moves0.append(move)
        
        elif classtype==b'\x42\x2C\x00\x00': 
            time1=struct.unpack('>f',dancedata.read(4))[0]
            struct.unpack('>f',dancedata.read(4))[0] #2.0
            time2=struct.unpack('>f',dancedata.read(4))[0]
            time3=struct.unpack('>f',dancedata.read(4))[0]
        elif classtype==b'\x41\xA0\x00\x00':
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            coachid=struct.unpack('>f',dancedata.read(4))[0] 
            pictovalue=struct.unpack('>f',dancedata.read(4))[0] 
            goldeffect=struct.unpack('>f',dancedata.read(4))[0]
            pictoname=mapname.lower()+'_'+str(int(pictovalue))
            shutil.copy('bin/picto.png', 'output/'+mapname+'/pictos/'+str(int(pictovalue))+'.png')
            picto={}
            picto['name']=str(int(pictovalue))
            picto['time']=int(starttime*multiplier)
            picto['duration']=int(duration*multiplier)

            pictos.append(picto)
        elif classtype==b'\x42\x0C\x00\x00': #from hip hop dance experience but idk what this class could be...
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            dancedata.read(4)
            #picto={}
            #picto['name']=str(int(pictovalue))
            #picto['time']=int(starttime*multiplier)
            #picto['duration']=int(duration*multiplier)

            #pictos.append(picto)

        elif classtype==b'\x42\x14\x00\x00': #freestyle text (hiphop dance experience)
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            dancedata.read(4)
            dancedata.read(4) #maybe another class for the freestyle text
            endtime=struct.unpack('>f',dancedata.read(4))[0]
            dancedata.read(4)
            duration=endtime-starttime
            hideui.append({"time": int(starttime*multiplier),"duration": int(duration*multiplier)})
        elif classtype==b'\x41\xD8\x00\x00': #pictos (jdkids 1)
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            hash2=dancedata.read(4)
            if hash2==b'\x00\x00\x00\x00': #sfx from the game being used as ambs. (smurfs)
                continue
                #amb={}
                #amb['name']='smurfs_applause'
                #amb['time']=int(starttime*multiplier)
                #amb['duration']=8000
                #amb['stopsOnEnd']=0

                #shutil.copy('bin/smurfs_applause.wav', 'output/'+mapname+'/amb/smurfs_applause.wav')
                #ambs.append(amb)
            else:
                pictovalue=struct.unpack('>f',dancedata.read(4))[0]
                dancedata.read(4)
                pictoeffect=struct.unpack('>f',dancedata.read(4))[0] #0 = no effect, 1 = chorus effect, 2 = gold move effect
                pictoname=mapname.lower()+'_'+str(int(pictovalue))
                shutil.copy('bin/picto.png', 'output/'+mapname+'/pictos/'+str(int(pictovalue))+'.png')
                picto={}
                picto['name']=str(int(pictovalue))
                picto['time']=int(starttime*multiplier)
                picto['duration']=1959

                pictos.append(picto)

                if int(pictoeffect)==2 and setting['goldEffectType']=='picto':
                    goldeffect={}
                    goldeffect['time']=int(starttime*multiplier)
                    goldeffect['duration']=1959
                    goldeffect['effectType']=1

                    goldmoves.append(goldeffect)
        elif classtype==b'\x42\x08\x00\x00': #moves (jdkids 1)
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            gamever=struct.unpack('>f',dancedata.read(4))[0]
            endtime=struct.unpack('>f',dancedata.read(4))[0]
            duration=endtime-starttime
            dancedata.read(4) #unknown
            dancedata.read(4)
            dancedata.read(4)
            movevalue=struct.unpack('>f',dancedata.read(4))[0]
            dancedata.read(4)
            goldmove=struct.unpack('>f',dancedata.read(4))[0]
            dancedata.read(4)
            if int(gamever)==8:
                continue
            else:
                dancedata.read(4)
            movename=mapname.lower()+'_'+str(int(movevalue))
            shutil.copy('bin/move.msm', 'output/'+mapname+'/moves/'+movename+'.msm')
            move={}
            move['name']=movename
            move['time']=int(starttime*multiplier)
            move['duration']=int(duration*multiplier)
            if int(goldmove)==2:
                move['goldMove']=1

                if setting['goldEffectType']=='move':
                    goldeffect={}
                    goldeffect['time']=int(starttime*multiplier)
                    goldeffect['duration']=1959
                    goldeffect['effectType']=1

                    goldmoves.append(goldeffect)
        
            #moves0.append(move)
        elif classtype==b'\x3F\x80\x00\x00':
            dancedata.read(4)
        elif classtype==b'\x41\x00\x00\x00':
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
        elif classtype==b'\x41\xF0\x00\x00':
            dancedata.read(4)
            dancedata.read(4)
        elif classtype==b'\x42\x30\x00\x00':
            dancedata.read(4)
            dancedata.read(4)
            starttime=struct.unpack('>f',dancedata.read(4))[0]
            endtime=struct.unpack('>f',dancedata.read(4))[0]
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            duration=endtime-starttime
        elif classtype==b'\x41\xE8\x00\x00': 
            dancedata.read(4)
            #dancedata.read(4)
            #dancedata.read(4)
            #dancedata.read(4)
            #dancedata.read(4)
            #dancedata.read(4)
            #dancedata.read(4)
            #dancedata.read(4)
            #dancedata.read(4)
        elif classtype==b'\x40\x40\x00\x00': 
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
            dancedata.read(4)
        elif classtype==b'':
            continue
        else:
            continue

except:
    pass

try:
    kdancedata=open('input/'+setting['mapInput']+'_360script.bin','rb')
    kdancedata.read(4)
    mapendtime=struct.unpack('>f',kdancedata.read(4))[0]
    mapendtime=int(mapendtime*1000)
    kdancedata.read(4)
    dancecount=struct.unpack('>f',kdancedata.read(4))[0]
    tapeversion=kdancedata.read(4)
    if tapeversion==b'\x41\xC8\x00\x00' or tapeversion==b'\x40\xC0\x00\x00' or tapeversion==b'\x41\x20\x00\x00': #smurfs, hip hop dance, jdkids 2 & 2014, jddisney 1 & 2
        kdancedata.read(24)

    for d in range(int(dancecount)):
        classtype=kdancedata.read(4)
        if classtype==b'\x41\xC8\x00\x00': #kinectmoves
            starttime=struct.unpack('>f',kdancedata.read(4))[0]
            gamever=struct.unpack('>f',kdancedata.read(4))[0]
            endtime=struct.unpack('>f',kdancedata.read(4))[0]
            duration=endtime-starttime
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4) 
            movevalue=struct.unpack('>f',kdancedata.read(4))[0]
            kdancedata.read(4) 
            goldmove=struct.unpack('>f',kdancedata.read(4))[0] #goldmove
            movename=mapname.lower()+'_'+str(int(movevalue))
            shutil.copy('bin/'+setting['gestureType'].lower()+'.gesture', 'output/'+mapname+'/gestures_'+setting['gestureType'].lower()+'/'+movename+'.gesture')
            move={}
            move['name']=movename
            move['time']=int(starttime*multiplier)
            move['duration']=int(duration*multiplier)
            if int(goldmove)==2:
                move['goldMove']=1

                if setting['goldEffectType']=='move':
                    goldeffect={}
                    goldeffect['time']=int(starttime*multiplier)
                    goldeffect['duration']=1959
                    goldeffect['effectType']=1

                    goldmoves.append(goldeffect)

            if int(gamever)==21 or int(gamever)==8: #jddisney 1 + 2 & jdkids 2014
                #kdancedata.read(56)
                coachid=struct.unpack('>f',kdancedata.read(4))[0]
                if int(coachid)==3:
                    kinect_moves0.append(move)
                elif int(coachid)==5:
                    kinect_moves1.append(move)
                elif int(coachid)==7:
                    kinect_moves0.append(move)
                    kinect_moves1.append(move)
                kdancedata.read(52)
            elif int(gamever)==20: #jdkids 2
                kinect_moves0.append(move)
                kdancedata.read(52)
            elif int(gamever)==9: #smurfs
                kinect_moves0.append(move)
                kdancedata.read(4)
                kdancedata.read(4)
            elif int(gamever)==10: #hiphop dance
                kinect_moves0.append(move)
                kdancedata.read(12)
            #kdancedata.read(24)

        elif classtype==b'\x41\xF0\x00\x00':
            starttime=struct.unpack('>f',kdancedata.read(4))[0]
            kdancedata.read(4)
            endtime=struct.unpack('>f',kdancedata.read(4))[0]
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)


        elif classtype==b'\x42\x18\x00\x00':
            time=struct.unpack('>f',kdancedata.read(4))[0]
            kdancedata.read(4)
        elif classtype==b'\x41\x00\x00\x00':
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
        elif classtype==b'\x41\x50\x00\x00':
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
            kdancedata.read(4)
        elif classtype==b'':
            continue
        else:
            continue
except:
    pass

try:
    pictodata=open('input/'+setting['mapInput']+'_ui.bin','rb')
    pictodata.read(4)
    pictodata.read(4)
    pictodata.read(4)
    dancecount=struct.unpack('>f',pictodata.read(4))[0]
    #game versions:
    #9: smurfs dance party
    #10: hip hop dance experience
    #21: jdkids 2014 & disney party 1 & 2
    for d in range(int(dancecount)):
        classtype=pictodata.read(4)
        if classtype==b'\x41\xA0\x00\x00' or classtype==b'\x42\x10\x00\x00' or classtype==b'\x42\x0C\x00\x00': #pictos
            starttime=struct.unpack('>f',pictodata.read(4))[0]
            coachid=struct.unpack('>f',pictodata.read(4))[0] 
            pictovalue=struct.unpack('>f',pictodata.read(4))[0] 
            goldeffect=struct.unpack('>f',pictodata.read(4))[0]
            pictoname=mapname.lower()+'_'+str(int(pictovalue))
            shutil.copy('bin/picto.png', 'output/'+mapname+'/pictos/'+str(int(pictovalue))+'.png')
            picto={}
            picto['name']=str(int(pictovalue))
            picto['time']=int(starttime*multiplier)
            picto['duration']=int(duration*multiplier)

            pictos.append(picto)

            if int(goldeffect)==2 and setting['goldEffectType']=='picto':
                goldeffect={}
                goldeffect['time']=int(starttime*multiplier)
                goldeffect['duration']=1959
                goldeffect['effectType']=1

                goldmoves.append(goldeffect)
        elif classtype==b'\x42\x00\x00\x00' or classtype==b'\x42\x1C\x00\x00' or classtype==b'\x42\x20\x00\x00': #hide user interface
            hideuitime=struct.unpack('>f',pictodata.read(4))[0]
            
            pictodata.read(4)
            pictodata.read(4)
            pictodata.read(4)

            if classtype==b'\x42\x1C\x00\x00':
                hideuistarttime=hideuitime
            if classtype==b'\x42\x20\x00\x00':
                hideuiendtime=hideuitime
            if classtype==b'\x42\x00\x00\x00':
                hideuiendduration=hideuitime
        elif classtype==b'':
            continue
        else:
            continue

    hideui.append({"time": 0,"duration": int(hideuistarttime*multiplier)})
    hideui.append({"time": int(hideuiendtime*multiplier),"duration": int(hideuiendduration*multiplier)})

except:
    pass

try: #dumping every language for lyrics
    lyrictextdataname='input/'+setting['mapInput']+'_lylic_data.bin'
    if setting['mapInput']+'_lylic_data_eng.bin' in os.listdir('input'):
        lyrictextdataname='input/'+setting['mapInput']+'_lylic_data_eng.bin'
    lyrictextdata=open(lyrictextdataname,'rb')
    lyrictextdata.read(2)
    textcount=struct.unpack('>h',lyrictextdata.read(2))[0]
    for lang in range(12):
        for t in range(textcount):
            lyrictext_len=struct.unpack('>h',lyrictextdata.read(2))[0]
            doublelen=lyrictext_len*2
            lyrictext=lyrictextdata.read(doublelen).decode('utf-16-be', 'backslashreplace')
            text[lang].append(lyrictext)

except:
    pass

try:
    lyricdataname='input/'+setting['mapInput']+'_lylic_script.bin'
    if setting['mapInput']+'_lylic_script_eng.bin' in os.listdir('input'):
        lyricdataname='input/'+setting['mapInput']+'_lylic_script_eng.bin'
    lyricdata=open(lyricdataname,'rb')
    lyriccount=struct.unpack('>f',lyricdata.read(4))[0]
    for t in range(int(lyriccount)):
        lyrictime=struct.unpack('>f',lyricdata.read(4))[0]
        lyricdata.read(4)#unknown
        lyricid=struct.unpack('>f',lyricdata.read(4))[0]#count
        lyricduration=struct.unpack('>f',lyricdata.read(4))[0]
        lyric={
        "time": int(lyrictime*multiplier),
        "duration": int(lyricduration*multiplier),
        "text": text[language][int(lyricid)],
        "isLineEnding": 1
        }
        lyrics.append(lyric)
    lyricdata.read(4)

except:
    pass

try:
    tracedata=open('input/'+setting['mapInput']+'_trace.bin','rb') #only used from smurfs
    tracedata.read(4)
    tracedata.read(2)
    tracecount=struct.unpack('>h',tracedata.read(2))[0]
    tracedata.read(4)
    tracedata.read(4)
    for t in range(tracecount):
        time=struct.unpack('>I',tracedata.read(4))[0]
        x=struct.unpack('>h',tracedata.read(2))[0]
        y=struct.unpack('>h',tracedata.read(2))[0]
        traces.append({"time": time, "x": x, "y": y})

except:
    pass

#currently the jdkids 1 tapes couldn't read the last move that's always a gold move so I decided to remove it from the array.
if tapeversion==b'\x41\xD0\x00\x00' and setting['goldEffectType']=='picto':
    del goldmoves[-1]

if setting['dumpTraces']==True:
    json.dump(traces,open('output/'+mapname+'/traces.json','w'))

#generating beats
bpm=float(setting['BPM'])
math=round(60000/bpm)
generatedbeats=0
beatamount=int(setting['beatAmount'])
milliseconds=int(setting['milliseconds'])

if setting['beatType']=='milliseconds':
    running=True
    for x in range(0,milliseconds,math):
        convertbeat=math*generatedbeats
        beats.append(x)
        generatedbeats+=1

if setting['beatType']=='beats':
    while generatedbeats<=beatamount:
        convertbeat=math*generatedbeats
        beats.append(convertbeat)
        generatedbeats+=1

indexcount=0
#multiplying 24 by each beat
for beat in beats:
    beatindexes.append(indexcount)
    indexcount+=24

if setting['dumpJSON']==True:
    json.dump(text,open('output/'+mapname+'/text.json','w'))
    json.dump(shakemoves,open('output/'+mapname+'/shakemoves.json','w'))
    json.dump(moves0,open('output/'+mapname+'/moves0.json','w'))
    json.dump(moves1,open('output/'+mapname+'/moves1.json','w'))
    json.dump(kinect_moves0,open('output/'+mapname+'/kinectmoves0.json','w'))
    json.dump(kinect_moves1,open('output/'+mapname+'/kinectmoves1.json','w'))
    json.dump(pictos,open('output/'+mapname+'/pictos.json','w'))
    json.dump(lyrics,open('output/'+mapname+'/lyrics.json','w'))
    json.dump(hideui,open('output/'+mapname+'/hideui.json','w'))
    json.dump(goldmoves,open('output/'+mapname+'/goldmoves.json','w'))

UbiArt.convert2UbiArt()

if setting['readLOGS']==True:
    readLogs()