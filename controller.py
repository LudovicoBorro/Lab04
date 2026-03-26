import time
import flet as ft
import model as md

class SpellChecker:

    def __init__(self, view):
        self._multiDic = md.MultiDictionary()
        self._view = view
        self._language = ""
        self._modality = ""

    def handleSentence(self, txtIn):
        txtIn = replaceChars(txtIn.lower())

        words = txtIn.split()
        paroleErrate = " - "

        match self._modality:
            case "Default":
                t1 = time.time()
                parole = self._multiDic.searchWord(words, self._language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Linear":
                t1 = time.time()
                parole = self._multiDic.searchWordLinear(words, self._language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Dichotomic":
                t1 = time.time()
                parole = self._multiDic.searchWordDichotomic(words, self._language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1
            case _:
                return None


    def printMenu(self):
        print("______________________________\n" +
              "      SpellChecker 101\n"+
              "______________________________\n " +
              "Seleziona la lingua desiderata\n"
              "1. Italiano\n" +
              "2. Inglese\n" +
              "3. Spagnolo\n" +
              "4. Exit\n" +
              "______________________________\n")

    def check_language(self, e):
        self._view._lvOut.controls.clear()
        corretto = False
        language = self._view._language
        if language.value.lower() == "english":
            self._language = "english"
            corretto = True
        elif language.value.lower() == "spanish":
            self._language = "spanish"
            corretto = True
        elif language.value.lower() == "italian":
            self._language = "italian"
            corretto = True

        if corretto:
            self._view._lvOut.controls.append(
                ft.Text("Selezione della lingua avvenuta correttamente!", color="green")
            )
            self._view.update()
        else:
            self._view._lvOut.controls.append(
                ft.Text("Selezione della lingua non avvenuta con successo!", color="red")
            )
            self._view.update()
        return corretto

    def check_modality(self, e):
        self._view._lvOut.controls.clear()
        corretto = False
        modality = self._view._modality
        if modality.value.lower() == "default":
            self._modality = "Default"
            corretto = True
        elif modality.value.lower() == "linear":
            self._modality = "Linear"
            corretto = True
        elif modality.value.lower() == "dichotomic":
            self._modality = "Dichotomic"
            corretto = True

        if corretto:
            self._view._lvOut.controls.append(
                ft.Text("Seleziona della modalità di ricerca avvenuta correttamente!", color="green")
            )
            self._view.update()
        else:
            self._view._lvOut.controls.append(
                ft.Text("Selezione della modalità di ricerca non avvenuta con successo!", color="red")
            )
            self._view.update()
        return corretto

    def handleSpellCheck(self, e):
        self._view._lvOut.controls.clear()
        self._view.update()

        if self._language == "":
            self._language = self._view._language.value.lower()
        if self._modality == "":
            self._modality = self._view._modality.value

        if not self._view._language.value in ["English", "Italian", "Spanish"]:
            self._view._lvOut.controls.append(
                ft.Text("Attenzione! Scegliere un linguaggio valido!", color="red")
            )
            self._view.update()
            return

        if not self._view._modality.value in ["Default", "Linear", "Dichotomic"]:
            self._view._lvOut.controls.append(
                ft.Text("Attenzione! Scegliere una modalità di ricerca valida!", color="red")
            )
            self._view.update()
            return

        if self._view._txtIn.value == "":
            self._view._lvOut.controls.append(
                ft.Text("Attenzione! Inserire una frase per eseguire lo Spell Check!", color="red")
            )
            self._view.update()
            return

        parole_errate, tempo = self.handleSentence(self._view._txtIn.value)

        self._view._lvOut.controls.append(
            ft.Text(f"Frase inserita: {self._view._txtIn.value}")
        )

        self._view._lvOut.controls.append(
            ft.Text(f"Parole errate: {parola.lower.strip()}")
            for parola in parole_errate
        )

        self._view._lvOut.controls.append(
            ft.Text(f"Tempo richiesto dalla ricerca: {tempo}")
        )

        self._view._txtIn.value = ""

        self._view.update()

def replaceChars(text):
    chars = "\\`*_{}[]()>#+-.!$?%^;,=_~"
    for c in chars:
        text = text.replace(c, "")
    return text