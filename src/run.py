import dependencies
import os

from core.soundlight import SoundLight

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        sl = SoundLight()

        #sl.addFileFromPath(r"resources/Oden & Fatzo X Camden Cox - Lady Love.mp3") 
        #sl.selectFile(0)
        #sl.analyze()
        
        sl.addFileFromPath(r"resources/Oden & Fatzo X Camden Cox - Lady Love.wav") 
        sl.selectFile(0)
        sl.analyze()
        sl.generate()
        sl.export(r"output/")
        
        #for key, value in sl._fm.getSelectedFile().getMetadata().items():
        #    print(f'{key}: {value}')

    except Exception as e:
        raise e