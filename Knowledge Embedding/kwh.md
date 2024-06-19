# Vervangen kilowattuur meter Q2 / Q3

![Image title](image/104036-2.png){ align=right }

## Beschrijving

In een MRA2 Laadpaal zijn 3 kilowatt uur meters aanwezig. De onderste is eigendom 
van de Netbeheerder deze mag alleen door de netbeheerder worden vervangen. 
De andere twee meters horen bij de twee laadporten, deze mogen wel worden 
vervangen.

## Benodigdheden

1. Vervangende KWH Meter (ABB)
2. Hoofdschakelaar vergrendeling
3. Duspol.
4. Kruiskop schroevendraaier
5. Kleine platte schroevendraaier (loshalen modbus draden)

## Toelichting

Een kilowattuur meter kan niet 1 op 1 uitgewisseld worden. Om de besturing van de laadpaal (eRTU print) te kunnen
laten communiceren met de meter wordt gebruik gemaakt van een Seriële RS-485 Modbus verbinding.

**Modbus**
Een (RTU-)Modbus verbinding is een seriële communicatieverbinding die wordt gebruikt om gegevens uit te wisselen
tussen verschillende apparaten. RTU staat voor "Remote Terminal Unit" en het is een protocol dat wordt gebruikt om
gegevens te verzenden over seriële lijnen. Dit protocol wordt vaak gebruikt in industriële toepassingen voor het
verzamelen en versturen van gegevens tussen verschillende apparaten, zoals energiemeters.

- **BAUD:** Dit verwijst naar de baudsnelheid, oftewel de snelheid waarmee de gegevens worden verzonden via
de verbinding.
- **RS-485:** Dit is het type seriële communicatieprotocol dat wordt gebruikt voor de verbinding. Het maakt bidirectionele communicatie mogelijk en maakt het mogelijk om over grote afstanden te communiceren.
- **Pariteit:** Dit is een controlemechanisme dat wordt gebruikt om ervoor te zorgen dat de gegevensoverdracht 
nauwkeurig is. Het kan instellingen hebben zoals 'even', 'oneven' of 'geen' om de controle aan te geven.
- **Adres:** Dit is het unieke identificatienummer dat aan elk apparaat in het netwerk wordt toegewezen, zodat 
de communicatie kan plaatsvinden tussen specifieke apparaten

## Stappen plan

!!! abstract annotate "Start het instel menu"

    1. Druk lang op de knop 'OK'
    2. Druk op de knop 'Pijltje' tot er 'SET' in beeld verschijnt
        1. ![Set](image/set.thumbnail.png) 
    3. Druk kort op 'OK'

!!! abstract annotate "RS-485 verbinding instellen"
 
    1. Druk op de knop ‘Pijltje’ tot ‘RS-485’ in beeld komt
        1. ![RS-485](image/rs485.thumbnail.png)
    2. Druk kort op ‘OK’

!!! abstract annotate "Protocol instellen"

    1. Druk op de knop ‘Pijltje’ tot ‘Protoc’ in beeld komt
        1. ![Protoc](image/protoc.thumbnail.png)
    2. Druk kort op ‘OK’
    3. Druk op de knop ‘SET’ (tekst gaat knipperen)
    4. Druk op de knop ‘Pijltje’ tot ‘Modbus’ in beeld komt
        1. ![Modbus](image/Modbus.thumbnail.png)
    5. Druk kort op ‘OK’ om de keuze vast te leggen.
        > Als de meter van Protocol moet wisselen kan het zijn dat de 
        > meter vanzelf opnieuw opstart. Dit is normaal. 
        > Volg dan de stappen 1 en 2 ga daarna verder met stap 4

    6. Druk lang op ‘OK’ om terug te keren naar het menu

!!! abstract annotate "Baudsnelheid instellen"

    1. Druk op de knop 'pijltje' tot 'BAUD' in beeld komt
        1. ![](image/baud.thumbnail.png)
    2. Druk kort op 'OK'
    3. Druk op de 'Set' knop (tekst gaat knipperen)
    4. Druk op de knop 'Pijltje' totdat '38400' in beeld komt
        1. ![](image/baudrate.thumbnail.png)
    5. Druk kort op 'OK' om de keuze vast te leggen
    6. Druk lang op 'OK' om terug te keren naar het menu

!!! abstract annotate "Modbus adres instellen"

    1. Druk op de knop 'Pijltje' tot 'Addres' in beeld komt
        1. ![Adres](image/Address.thumbnail.png)
    2. Druk kort op 'OK'
    3. Druk de knop 'SET' (tekst gaat knipperen)
    4. Druk op de knop 'Pijltje' om een adres te kiezen
        1. ![Adres 2](image/Address-2%20.thumbnail.png)
        
        > Bij twijfel gebruik adres 2, de meeste palen zijn van het type MRA

        |Lader type|Adres|
        | -------- |-----|
        |PRO       | 1   |
        |MRA       | 2   |
        |FKN       | 9   |

    5. Druk kort op 'OK' om de keuze vast te leggen
    6. Druk lang op 'OK' om terug te keren naar het menu
        

!!! abstract annotate "Parity"

    1. Druk op de knop 'Pijltje' tot 'Parity' in beeld komt
        1. ![](image/Parity.thumbnail.png)
    2. Druk kort op 'OK'
    3. Druk op de knop 'SET' (tekst gaat knipperen)
    4. Druk op de knop 'Pijltje' tot 'None' in beeld komt.
        1. ![](image/none.thumbnail.png)
    5. Druk kort op 'OK' om de keuze vast te leggen
    6. Druk 4x lang op 'OK' met ca 1 seconde interval om terug te keren naar het begin scherm.
        1. ![Beginscherm](image/Beginscherm.thumbnail.png)