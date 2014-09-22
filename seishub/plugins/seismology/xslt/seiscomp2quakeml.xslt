<?xml version="1.0" encoding="utf-8"?>
<!-- author: Tobias Megies, 2014 (megies@geophysik.uni-muenchen.de) -->
<xsl:stylesheet version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:sc3="http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.7"
        xmlns="http://quakeml.org/xmlns/bed/1.2">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml" method="xml" />

    <xsl:variable name="SMIROOT">smi:de.erdbeben-in-bayern</xsl:variable>

<!-- root template -->
    <xsl:template match="/">
        <xsl:apply-templates select="/sc3:seiscomp/sc3:EventParameters" />
    </xsl:template>

<!-- general structure template -->
    <xsl:template match="/sc3:seiscomp/sc3:EventParameters">
        <xsl:variable name="EVENTID">
            <xsl:value-of select="sc3:event/@publicID" />
        </xsl:variable>
        <xsl:variable name="ORIGINID">
            <xsl:value-of select="sc3:event/sc3:preferredOriginID" />
        </xsl:variable>
        <xsl:variable name="MAGNITUDEID">
            <xsl:value-of select="sc3:event/sc3:preferredMagnitudeID" />
        </xsl:variable>

        <q:quakeml xmlns:q="http://quakeml.org/xmlns/quakeml/1.2"
                   xmlns:edb="http://erdbeben-in-bayern.de/xmlns/0.1"
                   xmlns="http://quakeml.org/xmlns/bed/1.2">
        <eventParameters publicID="smi:de.erdbeben-in-bayern/catalog/{$EVENTID}">
        <event>
            <xsl:attribute name="publicID">
                <xsl:value-of select="$SMIROOT"/>/event/<xsl:value-of select="$EVENTID"/>
            </xsl:attribute>
            <xsl:apply-templates select="sc3:event/*" />
            <!-- origin and magnitude -->
            <xsl:if test="sc3:origin[@publicID=$ORIGINID]">
            <origin>
                <xsl:attribute name="publicID">
                    <xsl:value-of select="$SMIROOT"/>/origin/<xsl:value-of select="translate($ORIGINID, '#', '/')"/>
                </xsl:attribute>
                <xsl:apply-templates select="sc3:origin[@publicID=$ORIGINID]/*[not(self::sc3:stationMagnitude or self::sc3:magnitude)]" />
            </origin>
            </xsl:if>
            <xsl:if test="sc3:origin/sc3:magnitude[@publicID=$MAGNITUDEID]">
            <magnitude>
                <xsl:attribute name="publicID">
                    <xsl:value-of select="$SMIROOT"/>/magnitude/<xsl:value-of select="translate($MAGNITUDEID, '#', '/')"/>
                </xsl:attribute>
                <xsl:apply-templates select="sc3:origin/sc3:magnitude[@publicID=$MAGNITUDEID]/*" />
            </magnitude>
            </xsl:if>
            <!-- picks -->
            <xsl:for-each select="sc3:pick">
                <xsl:variable name="PICKID">
                    <xsl:value-of select="translate(@publicID, '#', '/')" />
                </xsl:variable>
            <pick publicID="smi:de.erdbeben-in-bayern/pick/{$PICKID}">
                <xsl:apply-templates select="./*" />
            </pick>
            </xsl:for-each>
            <!-- amplitudes -->
            <xsl:for-each select="sc3:amplitude">
                <xsl:variable name="AMPLITUDEID">
                    <xsl:value-of select="translate(@publicID, '#', '/')" />
                </xsl:variable>
            <amplitude publicID="smi:de.erdbeben-in-bayern/amplitude/{$AMPLITUDEID}">
                <xsl:apply-templates select="./*" />
            </amplitude>
            </xsl:for-each>
            <!-- station magnitudes -->
            <xsl:for-each select="sc3:origin[@publicID=$ORIGINID]/sc3:stationMagnitude">
                <xsl:variable name="STATIONMAGNITUDEID">
                    <xsl:value-of select="translate(@publicID, '#', '/')" />
                </xsl:variable>
            <stationMagnitude publicID="smi:de.erdbeben-in-bayern/station_magnitude/{$STATIONMAGNITUDEID}">
                <!-- originID missing.. reconstruct it -->
                <originID><xsl:value-of select="$SMIROOT"/>/origin/<xsl:value-of select="substring-before($STATIONMAGNITUDEID, '/staMag')"/></originID>
                <xsl:apply-templates select="./*" />
            </stationMagnitude>
            </xsl:for-each>
            <!-- custom namespace additions -->
            <edb:public>false</edb:public>
            <edb:evaluationMode>automatic</edb:evaluationMode>
        </event>
        </eventParameters>
        </q:quakeml>
    </xsl:template>
 
<!-- template to copy all elements by default -->
    <xsl:template match="*">
        <xsl:element name="{local-name()}">
            <xsl:apply-templates select="@* | node()"/>
        </xsl:element>
    </xsl:template>

<!-- template to copy all attributes by default -->
    <xsl:template match="@*">
        <xsl:attribute name="{local-name()}">
            <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>

<!-- template to copy any rest of the nodes by default -->
    <xsl:template match="comment() | text() | processing-instruction()">
        <xsl:copy/>
    </xsl:template>

<!-- Custom rules for some nodes -->
    <!-- map various non-conform resourceIDs -->
    <xsl:template match="sc3:event/sc3:preferredOriginID">
        <preferredOriginID><xsl:value-of select="$SMIROOT"/>/origin/<xsl:value-of select="translate(., '#', '/')"/></preferredOriginID>
    </xsl:template>
    <xsl:template match="sc3:event/sc3:preferredMagnitudeID">
        <preferredMagnitudeID><xsl:value-of select="$SMIROOT"/>/magnitude/<xsl:value-of select="translate(., '#', '/')"/></preferredMagnitudeID>
    </xsl:template>
    <xsl:template match="sc3:origin/sc3:methodID">
        <methodID><xsl:value-of select="$SMIROOT"/>/location_method/<xsl:value-of select="translate(., '#', '/')"/></methodID>
    </xsl:template>
    <xsl:template match="sc3:origin/sc3:earthModelID">
        <earthModelID><xsl:value-of select="$SMIROOT"/>/earth_model/<xsl:value-of select="translate(., '#', '/')"/></earthModelID>
    </xsl:template>
    <xsl:template match="sc3:agencyID">
        <agencyID><xsl:value-of select="$SMIROOT"/>/agency/<xsl:value-of select="translate(., '#', '/')"/></agencyID>
    </xsl:template>
    <xsl:template match="sc3:pickID">
        <pickID><xsl:value-of select="$SMIROOT"/>/pick/<xsl:value-of select="translate(., '#', '/')"/></pickID>
    </xsl:template>
    <xsl:template match="sc3:magnitude/sc3:methodID">
        <methodID><xsl:value-of select="$SMIROOT"/>/magnitude_method/<xsl:value-of select="translate(., '# ', '/_')"/></methodID>
    </xsl:template>
    <xsl:template match="sc3:stationMagnitudeID">
        <stationMagnitudeID><xsl:value-of select="$SMIROOT"/>/station_magnitude/<xsl:value-of select="translate(., '#', '/')"/></stationMagnitudeID>
    </xsl:template>
    <xsl:template match="sc3:amplitudeID">
        <amplitudeID><xsl:value-of select="$SMIROOT"/>/amplitude/<xsl:value-of select="translate(., '#', '/')"/></amplitudeID>
    </xsl:template>
    <xsl:template match="sc3:pick/sc3:methodID">
        <methodID><xsl:value-of select="$SMIROOT"/>/pick_method/<xsl:value-of select="translate(., '#', '/')"/></methodID>
    </xsl:template>
    <!-- quakeml has no "modificationTime" tag, use custom namespace -->
    <xsl:template match="sc3:creationInfo/sc3:modificationTime">
        <sc3:modificationTime><xsl:value-of select="."/></sc3:modificationTime>
    </xsl:template>
    <!-- arrivals lack the mandatory publicID, generate one -->
    <xsl:template match="sc3:arrival">
        <arrival>
        <xsl:attribute name="publicID">
            <xsl:value-of select="$SMIROOT"/>/arrival/<xsl:value-of select="./sc3:pickID"/>
        </xsl:attribute>
        <xsl:apply-templates select="./*"/>
        </arrival>
    </xsl:template>
    <!-- depth values seem to be in km (quakeml is in m) -->
    <xsl:template match="sc3:origin/sc3:depth/sc3:value">
        <value><xsl:value-of select=". * 1000"/></value>
    </xsl:template>
    <xsl:template match="sc3:origin/sc3:depth/sc3:uncertainty">
        <uncertainty><xsl:value-of select=". * 1000"/></uncertainty>
    </xsl:template>
    <!-- time window begin time seems to always be negative (quakeml is positive) -->
    <xsl:template match="sc3:timeWindow/sc3:begin">
        <begin><xsl:value-of select=". * -1"/></begin>
    </xsl:template>
    <!-- some subtags have different names -->
    <xsl:template match="sc3:magnitude/sc3:magnitude">
        <mag><xsl:apply-templates select="./*"/></mag>
    </xsl:template>
    <xsl:template match="sc3:stationMagnitude/sc3:magnitude">
        <mag><xsl:apply-templates select="./*"/></mag>
    </xsl:template>
    <xsl:template match="sc3:amplitude/sc3:amplitude">
        <genericAmplitude><xsl:apply-templates select="./*"/></genericAmplitude>
    </xsl:template>
    <xsl:template match="sc3:arrival/sc3:weight">
        <timeWeight><xsl:value-of select="."/></timeWeight>
    </xsl:template>

<!-- Rules to omit some nodes -->
    <xsl:template match="sc3:originReference"></xsl:template>

</xsl:stylesheet>
