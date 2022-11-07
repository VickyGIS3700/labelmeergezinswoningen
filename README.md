# Labelen van meergezinswoningen
Script labelen meergezinswoningen - data adressen Informatie Vlaanderen <br>
*script van Reginald Carlier, GIS deskundige Ingelmunster*

Dit script maakt een label waarop de bussen op de verschillende verdiepingen gerangschikt worden volgens verdiep
mgz_straathuisnr is de tabel met uniek straathuisnr voor meergezinswoningen 
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

Voorbeeld labeling:
![image](https://user-images.githubusercontent.com/32510519/200315129-bce3a225-5668-4c9e-9948-5821d9a968a0.png)
