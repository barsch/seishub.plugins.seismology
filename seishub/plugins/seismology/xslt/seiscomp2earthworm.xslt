<?xml version = '1.0' encoding = 'UTF-8'?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml"
        method="xml" />
    <xsl:template match="/">
        <xsl:apply-templates
            select="/seiscomp/EventParameters/origin[@publicID=string(../event/preferredOriginID/text())]"
         />
    </xsl:template>
    <xsl:template
        match="/seiscomp/EventParameters/origin[@publicID=string(../event/preferredOriginID/text())]">
        <event>
            <xsl:attribute name="source">seiscomp3</xsl:attribute>
            <event_id>
                <xsl:value-of select="../event/@publicID" />
            </event_id>
            <event_type>
              <value><xsl:value-of select="evaluationMode" /></value>
              <account>seiscomp3</account>
              <user/>
              <public>False</public>
            </event_type>
            <xsl:for-each select="../pick">
                <pick>
                    <waveform>
                        <xsl:attribute name="networkCode">
                            <xsl:value-of select="waveformID/@networkCode" />
                        </xsl:attribute>
                        <xsl:attribute name="stationCode">
                            <xsl:value-of select="waveformID/@stationCode" />
                        </xsl:attribute>
                        <xsl:attribute name="locationCode">
                            <xsl:value-of select="waveformID/@locationCode" />
                        </xsl:attribute>
                    </waveform>
                    <time>
                        <value>
                            <xsl:value-of select="time/value" />
                        </value>
                        <uncertainty>0.000000</uncertainty>
                    </time>
                    <phaseHint>
                        <xsl:value-of select="phaseHint" />
                    </phaseHint>
                </pick>
            </xsl:for-each>
            <origin>
                <time>
                    <value>
                        <xsl:value-of select="time/value" />
                    </value>
                    <uncertainty>
                        <xsl:value-of select="time/lowerUncertainty" />
                    </uncertainty>
                </time>
                <latitude>
                    <value>
                        <xsl:value-of select="latitude/value" />
                    </value>
                    <uncertainty>
                        <xsl:value-of select="latitude/lowerUncertainty" />
                    </uncertainty>
                </latitude>
                <longitude>
                    <value>
                        <xsl:value-of select="longitude/value" />
                    </value>
                    <uncertainty>
                        <xsl:value-of select="longitude/lowerUncertainty" />
                    </uncertainty>
                </longitude>
                <depth>
                    <value>
                        <xsl:value-of select="depth/value" />
                    </value>
                    <uncertainty>
                        <xsl:value-of select="depth/lowerUncertainty" />
                    </uncertainty>
                </depth>
            </origin>
            <xsl:for-each
                select="magnitude[@publicID=string(../../event/preferredMagnitudeID/text())]">
                <magnitude>
                    <mag>
                        <value>
                            <xsl:value-of select="magnitude/value" />
                        </value>
                        <uncertainty>
                            <xsl:value-of select="magnitude/lowerUncertainty"
                             />
                        </uncertainty>
                    </mag>
                    <type>
                        <xsl:value-of select="type" />
                    </type>
                    <station_count>
                        <xsl:value-of select="stationCount" />
                    </station_count>
                </magnitude>
            </xsl:for-each>
        </event>
    </xsl:template>
</xsl:stylesheet>
