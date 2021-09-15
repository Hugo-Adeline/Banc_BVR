from fpdf import FPDF  # fpdf class
from time import localtime
import os
from PDF.SendEmail import SendDiag
import subprocess

pdf_w = 210
pdf_h = 297

class PDF(FPDF):
    def setup(self):

        # Création des variables de comptage d'erreur (permet d'incrémenter la ligne d'écriture après l'ajout d'une erreur)
        self.errAut = 0
        self.errSel = 0
        self.errEng = 0
        self.errEmb = 0
        self.errPre = 0
        # Variable utilisée pour stocker le nom du robot qui sera ajouter au titre dans add_robot()
        self.robotName = 'None'
        # Définition de l'emplacement actuel du programme (nécessaire à l'enregistrement du PDF)
        self.filepath = os.path.dirname(os.path.abspath(__file__))

        # Cadre en-tête
        self.set_line_width(1)                          #Epaisseur de la ligne
        self.set_fill_color(r= 175)                     #Couleur du remplissage GRIS
        self.rect(40.0, 10.0, 130.0, 40, style= 'DF')   #Création d'un cadre rectangulaire
        self.set_fill_color(r= 255)                     #Couleur du remplissage BLANC

        # En-tête
        self.set_xy(0.0, 0.0)                                           #Emplacement du curseur
        self.set_font('Arial', 'B', 18)                                 #Définition de la police d'écriture
        self.cell(w= 210, h= 40, txt= "FICHE DIAGNOSTIC", align= 'C')   #Création d'une zone de Texte
        self.set_font('Arial', 'B', 14)
        self.set_xy(47.0, 15.0)
        self.cell(w= 50, h= 32, txt= "Date:")
        self.set_xy(110.0, 15.0)
        self.cell(w= 50, h= 32, txt= "Robot:")
        self.set_xy(70.0, 25.0)
        self.cell(w= 50, h= 32, txt= "Opérateur:.............................")

        # Création de la date au format JJ/MM/AAAA
        # Récupération des données
        t = localtime()
        self.day = str(t.tm_mday)
        self.month = str(t.tm_mon)
        self.year = str(t.tm_year)
        self.hour = str(t.tm_hour)
        self.minute = str(t.tm_min)
        # Formalisation des données avec ajout d'un 0_ pour les entiers à un chiffre
        self.date = ''
        if len(self.day) == 1:
            self.day = '0' + self.day
        self.date += self.day + '/'
        if len(self.month) == 1:
            self.month = '0' + self.month
        self.date += self.month + '/' + self.year + ' '
        if len(self.hour) == 1:
            self.hour = '0' + self.hour
        self.date += self.hour + ':'
        if len(self.minute) == 1:
            self.minute = '0' + self.minute
        self.date += self.minute
        #Affichage de la date
        self.set_xy(61.0,15.0)
        self.set_font('Arial', '', 14)
        self.cell(w= 210, h= 32, txt= self.date)

        # Cadres contenant le diagnostic
        self.set_line_width(0.5)

        offset = 2.5

        self.set_fill_color(r= 215)
        self.rect(25.0, 60.0 + 5, 80.0 - offset, 60.0, style= 'DF')
        self.rect(105.0 + offset, 60.0 + 5, 80.0 - offset, 60.0, style= 'DF')
        self.rect(105.0 + offset, 120.0 + 5 + offset, 80.0 - offset, 60.0, style= 'DF')
        self.rect(25.0, 120.0 + 5 + offset, 80.0 - offset, 60.0, style= 'DF')
        self.rect(25.0, 180.0 + 5 + 2*offset, 80.0 - offset, 60.0, style= 'DF')

        h = 11
        self.set_fill_color(r= 175)
        self.rect(25.0, 60.0 + 5, 80.0 - offset, h, style= 'DF')
        self.rect(105.0 + offset, 60.0 + 5, 80.0 - offset, h, style= 'DF')
        self.rect(105.0 + offset, 120.0 + 5 + offset, 80.0 - offset, h, style= 'DF')
        self.rect(25.0, 120.0 + 5 + offset, 80.0 - offset, h, style= 'DF')
        self.rect(25.0, 180.0 + 5 + 2*offset, 80.0 - offset, h, style= 'DF')

        self.set_fill_color(r= 255)
        self.rect(105.0 + offset, 180.0 + 5 + 2*offset, 80.0 - offset, 60.0, style= 'DF')

        self.set_line_width(0.4)

        self.rect(25.0, 84 + h + 5, 80.0 - offset, 36.0 - h, style= 'DF')
        self.rect(105.0 + offset, 84 + h + 5, 80.0 - offset, 36.0 - h, style= 'DF')
        self.rect(105.0 + offset, 144.0 + h + 5 + offset, 80.0 - offset, 36.0 - h, style= 'DF')
        self.rect(25.0, 144.0 + h + 5 + offset, 80.0 - offset, 36.0 - h, style= 'DF')
        self.rect(25.0, 204.0 + h + 5 + 2*offset, 80.0 - offset, 36.0 - h, style= 'DF')

        # Logo
        self.image(self.filepath + "/splashFARAL.png",        #Ajout du logo FARAL
                   x= 135, y= 261, w= 640/10, h=211/10)

        # Pied de page
        self.set_xy(20, 270)
        self.set_font('Arial', '', 10)
        self.cell(w= 50, h= 5, txt= "Banc d'essai robot (BVR) FARAL Automotive")

        # Textede la partie diagnostic
        self.set_font('Arial', 'B', 13)
        self.set_xy(25, 55.5 + 5)
        self.cell(w= 80 - offset, h= 20, txt= "Pression", align= 'C')
        self.set_xy(105 + offset, 55.5 + 5)
        self.cell(w= 80 - offset, h= 20, txt= "Sélection", align= 'C')
        self.set_xy(25, 115.5 + 5 + offset)
        self.cell(w= 80 - offset, h= 20, txt= "Embrayage", align= 'C')
        self.set_xy(105 + offset, 115.5 + 5 + offset)
        self.cell(w= 80 - offset, h= 20, txt= "Engagement", align= 'C')
        self.set_xy(25, 175.5 + 5 + offset*2)
        self.cell(w= 80 - offset, h= 20, txt= "Autre", align= 'C')

        self.set_font('Arial', 'U', 10)
        self.set_xy(26.0, 88.0 + 5)
        self.cell(w= 50, h= 20, txt= "Commentaires:")
        self.set_xy(106.0 + offset, 88.0 + 5)
        self.cell(w= 50, h= 20, txt= "Commentaires:")
        self.set_xy(26.0, 148.0 + 5 + offset)
        self.cell(w= 50, h= 20, txt= "Commentaires:")
        self.set_xy(106.0 + offset, 148.0 + 5 + offset)
        self.cell(w= 50, h= 20, txt= "Commentaires:")
        self.set_xy(26.0, 208.0 + 5 + offset*2)
        self.cell(w= 50, h= 20, txt= "Commentaires:")

        self.set_font('Arial', 'B', 11)
        self.set_xy(107.5 + offset, 180 + offset*2)
        self.cell(w= 50, h= 20, txt= "Validation de la conformité du robot:")
        self.set_font('Arial', 'B', 10)
        self.set_xy(121, 230 + offset*2)
        self.cell(w= 50, h= 20, txt= "Date de la certification:......................")


    def add_robot(self, name):

        # Ajout du nom du robot
        self.set_xy(128.0,15.0)
        self.set_font('Arial', '', 14)
        self.cell(w= 50, h= 32, txt= name)
        self.robotName = name


    def add_error(self, category, text):

        #Ajout des erreurs
        offset = 2.5
        self.set_font('Arial', 'I', 10)
        if category == 'Pression':
            self.set_xy(27.5, 65.5 + self.errPre * 5 + 5)
            self.errPre += 1
        if category == 'Sélection':
            self.set_xy(107.5 + offset, 65.5 + self.errSel * 5 + 5)
            self.errSel += 1
        if category == 'Embrayage':
            self.set_xy(27.5, 125.5 + self.errEmb * 5 + 5 + offset)
            self.errEmb += 1
        if category == 'Engagement':
            self.set_xy(107.5 + offset, 125.5 + self.errEng * 5 + 5 + offset)
            self.errEng += 1
        if category == 'Autre':
            self.set_xy(27.5, 185.5 + self.errAut * 5 + 5 + offset*2)
            self.errAut += 1
        self.cell(w= 210, h= 20, txt= '- ' + text)


    def set_receiver_email(self, receiver_email):

        # Création de la variable contenant l'email du destinataire
        self.receiver_email = receiver_email


    def done(self):

        # Sauvegarde du PDF au format "Fiche_Diag_Robot_AAAA.MM.JJ.HHhMM_1.pdf" avec un système d'incrémentation en cas de duplicata

        # Création de la date au format AAAA.MM.JJ.HHhMM en utilisant les variables de la fonction setup (ligne 42)
        date = self.year + '.' + self.month + '.' + self.day + '.' + self.hour + 'h' + self.minute
        # Création du nom du fichier avec la date
        name = 'Fiche_Diag_' + self.robotName + '_' + date
        # Détermination de l'indice final en fonction de l'existence d'un fichier identique
        i = 1
        while name + '_' + str(i) + '.pdf' in os.popen("dir " + self.filepath + '/DiagReport').read():
            i += 1
        # Ajout de l'indice final avec l'extension
        name = name + '_' + str(i) + '.pdf'
        # Création du fichier PDF
        self.output(self.filepath + '/DiagReport/' + name)

        # Création d'un backup sur la clé USB
        disk = os.popen("ls /media/pi").read()
        if disk != '':
            disk = disk[:-1]
            self.backupPath = '/media/pi/' + disk + '/raspberry/Banc_Robot/Software/PDF/DiagReport/'
            if self.backupPath != None:
                command = 'cp ' + self.filepath + '/DiagReport/' + name + " " + self.backupPath
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                process.communicate()[0]

        # Envoi du diagnostic avec 5 tentatives
        for i in range(5):
            retour = SendDiag(name, self.date, self.receiver_email)
            if retour:
                status = True
                break
            else:
                status = False
        # Retour du status de l'envoi
        if not status:
            return False
        return True

# Code de test qui génère un rapport à l'éxecution du fichier (pratique pour vérifier les changements de la forme du pdf)
"""
pdf = PDF() # pdf object
pdf.add_page()
pdf.setup()
pdf.add_robot('PA6')
for i in range(1):
    pdf.add_error('Pression', 'Fonctionnement nominal')
    pdf.add_error('Sélection', 'Fonctionnement nominal')
    pdf.add_error('Embrayage', 'Fonctionnement nominal')
    pdf.add_error('Engagement', 'Fonctionnement nominal')
    pdf.add_error('Autre', 'Fonctionnement nominal')
pdf.done()
"""
