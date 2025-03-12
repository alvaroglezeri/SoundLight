<!--- Link references --->
[1]: https://github.com/mir-aidj/all-in-one (GitHub: All-in-One)

<!--- --->
---
# **Analysis Phase**

The analysis phase is the first step in the Soundlight processing chain. It is in charge of extracting all relevant song artifacts and saving the results.

It is composed of the following tasks:

## 1. Beat and Key recognition  
In this task, a basic analysis of key, BPM and beat offset are performed, which constitutes the base of the song profile.

The key analysis is performed using `librosa`'s built in methods.


## 2. Phrase Analysis  
In this task, the musical phrases of the song are extracted and recorded from the source. This increments the coherence of the generation, as it provides valuable structural data for future steps.

This task employs the methods provided by [All-in-One][1] to perform its analysis.


## 3. Stemming (Source Separation)  
In this task, the source song is separated into stems (vocals, melody, drums and other). This task is important because it allows the different parts of the song to be treated separately, giving way to advanced generation that would otherwise be impossible. It is also decided here if each stem contains valuable information, and if not, it is discarded.


## 4. Stem Pulse and Frequency mapping  
In this task, stems are analyzed separately for sound pulses. From those, frequency and volume are extracted, and recorded individually for further use.


## 5. Profile Construction  
In this task, the results of all preceding tasks are incorporated into the song profile, which will be feeded to the next step's agents. This is important because it avoids having to reanalyze songs, by saving the results into a reusable format.


## 6. Database Registration  
In this task, the profile is optionally registered in a database for later library management.

---
