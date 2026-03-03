import re

def main():
    # 1. Read Markdown
    with open('research/john_8_32_translations.md', 'r') as f:
        md = f.read()
    
    # 2. Prepare plain text for manuscript.txt
    txt_content = """
═══════════════════════════════════════════════════════════════

     APPENDIX 11
     
     The Truth That Liberates (A Translation Compendium on John 8:32)

═══════════════════════════════════════════════════════════════


Note on inclusion: This compendium was compiled by Claude Opus 4.6 
during the research phase of this project. It was selected and added 
to the final manuscript by the author and Gemini 3.1 Pro as a thematic 
conclusion. The entire booklet is an exercise in pursuing historical 
truth over emotionally compelling narratives, and this verse reminds 
us why that matters: truth is what liberates. Furthermore, the Hebrew 
translation's use of the Exodus word for freedom (ḥerut) perfectly 
ties the search for truth back to the Passover (Pascha) event itself.


"""
    
    # Simple markdown to plain text conversion
    lines = md.split('\n')
    for line in lines[1:]: # Skip the first # title
        if line.startswith('## '):
            txt_content += '\n\n' + line[3:].upper() + '\n\n'
        elif line.startswith('### '):
            txt_content += '\n' + line[4:] + '\n\n'
        elif line.startswith('> '):
            txt_content += '  ' + line[2:] + '\n'
        elif line.startswith('**Note'):
            txt_content += '\n' + line.replace('**', '') + '\n'
        elif line.startswith('|'):
            txt_content += line + '\n'
        elif line.startswith('---'):
            txt_content += '\n⸻\n'
        else:
            # remove simple bold and italics
            l = line.replace('**', '').replace('*', '')
            txt_content += l + '\n'
            
    txt_content += '\n\n'

    with open('manuscript.txt', 'r') as f:
        ms = f.read()
    
    # insert before FOOTNOTES
    ms = ms.replace('═══════════════════════════════════════════════════════════════\n\n     FOOTNOTES', txt_content + '═══════════════════════════════════════════════════════════════\n\n     FOOTNOTES')
    
    with open('manuscript.txt', 'w') as f:
        f.write(ms)

    # 3. Prepare LaTeX content
    tex_content = r"""
\section*{Appendix 11}
\addcontentsline{toc}{section}{Appendix 11}
\markboth{Appendix 11}{Appendix 11}

\begin{center}
    {\Large\bfseries The Truth That Liberates}\\[0.5em]
    {\itshape A Translation Compendium on John 8:32}
\end{center}
\vspace{1em}

\begin{quote}
\small \textit{Note on inclusion:} This compendium was compiled by Claude Opus 4.6 during the research phase of this project. It was selected and added to the final manuscript by the author and Gemini 3.1 Pro as a thematic conclusion. The entire booklet is an exercise in pursuing historical truth over emotionally compelling narratives, and this verse reminds us why that matters: truth is what liberates. Furthermore, the Hebrew translation's use of the Exodus word for freedom (\textit{ḥerut}) perfectly ties the search for truth back to the Passover (Pascha) event itself.
\end{quote}
\vspace{1em}

\noindent\textit{Compiled for reference. Sources: Bible Gateway, BibleHub Interlinear, YouVersion/TPT, Delitzsch Hebrew NT, Dukhrana Peshitta, Bible Society in Israel}

\subsection*{Original Greek (NA28 / Nestle-Aland)}
\begin{quote}
\textbf{καὶ γνώσεσθε τὴν ἀλήθειαν, καὶ ἡ ἀλήθεια ἐλευθερώσει ὑμᾶς.}
\end{quote}

\textbf{Note:} The Greek verb \textit{ἐλευθερόω} (eleutheroō) means to liberate, to set free—cognate with \textit{ἐλευθερία} (eleutheria), freedom/liberty. The future indicative (\textit{gnōsesthe ... eleutherōsei}) frames both knowing and liberation as assured consequences, not mere possibilities.

\subsection*{Aramaic Peshitta (2nd–5th century AD)}
\begin{quote}
\textbf{ܘܬܶܕܥܽܘܢ ܫܪܳܪܳܐ ܘܗܽܘ ܫܪܳܪܳܐ ܢܚܰܪܰܪܟܽܘܢ}

``And you shall know the truth, and that truth shall set you free.''
\end{quote}

\textbf{Note on ܫܪܳܪܳܐ (shrārā):} The Aramaic word for truth derives from the root \textit{sh-r-r}, meaning to be firm, established, confirmed. It carries connotations of solidity and verification—truth as that which holds firm under scrutiny. This resonates with the Hebrew \textit{emet} (אמת) more directly than the Greek \textit{alētheia}, since Aramaic and Hebrew are sister Semitic languages. The Peshitta is the standard Bible of Syriac Christianity and was the scripture of the Eastern churches from late antiquity onward.

English translations from the Peshitta:
\begin{itemize}
    \item \textbf{Etheridge (1849):} ``and you shall know the truth, and the truth shall make you free.''
    \item \textbf{Murdock (1852):} ``and ye will know the truth; and the truth will make you free.''
    \item \textbf{Lamsa (1933):} ``And you will know the truth, and the truth will make you free.''
\end{itemize}

\subsection*{Hebrew Translations}
\textbf{Delitzsch Hebrew New Testament (Franz Delitzsch, 1877; rev. 1901)}
\begin{quote}
\textbf{\hebrewfont{וִידַעְתֶּם אֶת־הָאֱמֶת וְהָאֱמֶת תּוֹצִיאֲכֶם לְחֵרוּת׃}}

\textit{Vidaʿtem et-ha'emet, v'ha'emet totzi'akhem l'ḥerut.}

``And you shall know the truth, and the truth shall bring you out to freedom.''
\end{quote}

\textbf{Note on Delitzsch's rendering:} Delitzsch, a Christian Hebraist of the highest order, chose the hifʿil form of \textit{יצא} (yatzaʾ, ``to go out'') — \textit{תּוֹצִיאֲכֶם} — ``shall bring you out.'' This is the same verbal root used for the Exodus: God \textit{brought Israel out} (הוֹצִיא) of Egypt. The choice is theologically loaded, framing Jesus's promise of liberation through truth as a new Exodus. The word \textit{חֵרוּת} (ḥerut, ``freedom'') is the same word used in the Passover Haggadah and rabbinic literature for the freedom celebrated at Pesach.

\vspace{1em}
\textbf{Modern Hebrew (Bible Society in Israel, 1977)}
\begin{quote}
\textbf{\hebrewfont{וִידַעְתֶּם אֶת הָאֱמֶת וְהָאֱמֶת תְּשִׂימְכֶם לִבְנֵי חוֹרִין׃}}

\textit{Vidaʿtem et ha'emet, v'ha'emet t'simkhem livnei ḥorin.}

``And you shall know the truth, and the truth shall make you children of freedom.''
\end{quote}

\textbf{Note on the modern Hebrew idiom:} Where Delitzsch uses the Exodus verb הוציא + חרות, the Bible Society translation uses the rabbinic phrase \textbf{בְּנֵי חוֹרִין} (\textit{b'nei ḥorin}), literally ``sons/children of freedom'' — a technical term from the Mishnah (Avot 6:2) meaning ``free persons'' as opposed to slaves. The Mishnaic passage itself cites Exodus 32:16, reading \textit{ḥerut} (``freedom'') for \textit{ḥarut} (``engraved'') on the tablets: ``Read not `engraved' (\textit{ḥarut}) but `freedom' (\textit{ḥerut}), for no one is truly free except the one who occupies himself with Torah.'' The resonance with Jesus's words — that \textit{continuing in his word} leads to \textit{knowing truth} which leads to \textit{freedom} — could hardly be more striking.

\vspace{1em}
\textbf{A Note on Shem-Tov's Hebrew Matthew}\\
The Shem-Tov Hebrew Matthew (c. 1380, preserved by Rabbi Shem-Tov ben Isaac ben Shaprut in his polemical work \textit{Even Boḥan}) is the oldest extant Hebrew text of any Gospel. However, it contains \textbf{only the Gospel of Matthew}, not John. There is no Shem-Tov text of John 8:32. The Shem-Tov Matthew is nonetheless significant for the study of Hebrew Gospel traditions and the question of whether any Gospel originally circulated in a Semitic language. See George Howard's critical edition: \textit{Hebrew Gospel of Matthew} (Mercer University Press, 1995).

\subsection*{Latin Vulgate (Jerome, c. 382 AD)}
\begin{quote}
\textbf{et cognoscetis veritatem, et veritas liberabit vos.}

``And you shall know the truth, and the truth shall liberate you.''
\end{quote}

\subsection*{Translation Notes}

\textbf{``Make you free'' vs. ``Set you free'':} The older English translations (KJV, Wycliffe, Geneva, RSV, NRSV, NKJV) prefer ``make you free,'' while most modern translations (NIV, ESV, NASB 2020, CSB, NLT) use ``set you free.'' Both translate \textit{ἐλευθερώσει} (eleutherōsei). The shift reflects changing English idiom—``set free'' has become the more natural expression of liberation in contemporary English.

\textbf{``Know'' vs. ``Experience'' vs. ``Embrace'':} Most translations render \textit{γνώσεσθε} (gnōsesthe) as ``know,'' reflecting the Greek future indicative of \textit{γινώσκω} (ginōskō)—a word implying experiential, relational knowledge rather than mere intellectual awareness. Peterson's MSG uses ``experience for yourselves'' to capture this nuance. Simmons' TPT uses ``embrace,'' a more interpretive choice.

\textbf{The conditional context (v. 31):} The promise of v. 32 is conditional on v. 31 — ``If you continue in my word'' (ἐὰν ὑμεῖς μείνητε ἐν τῷ λόγῳ τῷ ἐμῷ). The truth that liberates is not abstract philosophical truth but truth \textit{abided in}, \textit{lived}, \textit{continued in}. This is critical for the book's argument about the relationship between doctrine held and doctrine lived.

\textbf{ἀλήθεια (alētheia) / אמת (emet) / ܫܪܪܐ (shrārā):} Three linguistic worlds converge on this single concept. In Greek philosophical usage, \textit{alētheia} means ``unconcealment'' or ``disclosure'' (from α-λήθη, ``un-forgetting'') — truth as reality unveiled. In Hebrew, \textit{emet} (אמת) derives from the root א-מ-נ (\textit{ʾ-m-n}), meaning firmness, faithfulness, reliability — truth as that which can be leaned on, the same root as \textit{amen}. In Aramaic, \textit{shrārā} (ܫܪܳܪܳܐ) from \textit{sh-r-r} means established, confirmed, made firm — truth as that which holds under testing. Jesus himself is identified as \textit{the} truth (John 14:6), making this verse simultaneously epistemological and personal.

\textbf{The Exodus typology in Hebrew:} Delitzsch's choice of \textit{תּוֹצִיאֲכֶם לְחֵרוּת} (totzi'akhem l'ḥerut — ``shall bring you out to freedom'') explicitly frames John 8:32 as a new Exodus. The verb \textit{הוציא} is the definitive Exodus verb (Exodus 20:2: ``I am the LORD your God who \textit{brought you out} of the land of Egypt, out of the house of slavery''). The modern Hebrew translation's use of \textit{בְּנֵי חוֹרִין} (b'nei ḥorin — ``children of freedom'') draws on the Passover Haggadah and Mishnah Avot 6:2, where Torah study itself is said to confer the status of a free person. For a book about the historical body of Christ and the liberation that truth brings, these Hebrew resonances are extraordinarily rich — they tie Jesus's words to the foundational Jewish narrative of God liberating his people from bondage.

\newpage
"""

    with open('pascha-not-easter-booklet.tex', 'r') as f:
        tex = f.read()
    
    tex = tex.replace('\\section{Glossary of Terms}', tex_content + '\\section{Glossary of Terms}')
    
    with open('pascha-not-easter-booklet.tex', 'w') as f:
        f.write(tex)

if __name__ == '__main__':
    main()
