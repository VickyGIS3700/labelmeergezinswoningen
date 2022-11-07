from qgis.utils import iface
from qgis.core import *

''' Dit script maakt een label waarop de bussen op de verschillende verdiepingen gerangschikt worden volgens verdiep '''

layers = [layer for layer in QgsProject.instance().mapLayers().values()]

''' laag met labels voor mgz '''
''' mgz_straathuisnr is de tabel met uniek straathuisnr voor meergezinswoningen 
deze tabel staat in een postgresql database. Het probleem dat zich stelde bij het gebruik van een geopackage of shapefile was
dat deze steeds gelocked werden bij het wijzigen.
De oorspronkelijke data werd gedownload van de CRAB WFS. In deze laag staat zowel een veld voor een busnummer alsook een veld
voor een appartementsnummer. De gegevens uit beide velden werden gecombineerd in één enkel veld: busnr
Daarnaast werd ook een veld aangemaakt straathuisnr. Dit veld dient om de unieke meergezinswoningen te filteren.
Eerst exporteerde ik de meergezinsadressen naar een postgres tabel adressen_met_busnr. Deze tabel filterde ik.
Hiervoor werd het QGIS algorithm 'Duplicaten verwijderen op attribuut' gebruikt. Zo bekom je een tabel waar er enkel één 
crabadres is per gebouw: mgz_straathuisnr. In deze tabel maak ik een veld label (varchar 255). Dit veld dient om een label aan te maken met 
onderstaand script. De oorspronkelijke crabadressen gebruikte ik om alle adressen te labelen met enkel het huisnummer
(huisnummer toont ook het bisnummer eg. 1A).
'''

mgz_straathuisnr = None
''' laag met busnummers '''
adressen_met_busnr = None

def get_items(mylist, letter):
  return [item for item in mylist if item[:2] == letter]


for lyr in layers:
    if lyr.name() == "mgz_straathuisnr":
        mgz_straathuisnr = lyr
    if lyr.name() == "adressen_met_busnr":
        adressen_met_busnr = lyr
        
prov = mgz_straathuisnr.dataProvider()
capa = prov.capabilities()
label = mgz_straathuisnr.fields().lookupField('label')
        
with edit(mgz_straathuisnr):
    for mgz in mgz_straathuisnr.getFeatures():
        labels = []
        straathuisnr = mgz["straathuisnr"]
        print(straathuisnr)
        for feat in adressen_met_busnr.getFeatures():
            strhnr = feat["straathuisnr"]
            if strhnr == straathuisnr:
                labels.append(feat["busnr"])
        labelstring = ''
        verdiepen = []
        for i in labels:
            vp = i[:2]
            verdiepen.append(vp)
        ''' vind unieke verdiepen '''
        unieke_verdiepen = [*set(verdiepen)]
        uv_rev_sorted = sorted(unieke_verdiepen, reverse=True)
        for vdp in uv_rev_sorted:
            verdiep = get_items(labels, vdp)
            verdiep = sorted(verdiep)
            print(verdiep)
            for v in verdiep:
                labelstring += ' '
                labelstring += v
            labelstring += '\n'
        print(labelstring)
        atts = {label:labelstring}
        if capa & QgsVectorDataProvider.ChangeAttributeValues:
            prov.changeAttributeValues({mgz.id(): atts})
        else:
            print("unable to change attribute")
    
    
print("klaar")
    
        
            
        
    