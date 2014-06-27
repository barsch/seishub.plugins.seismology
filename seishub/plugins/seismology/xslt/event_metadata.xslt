<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:q="http://quakeml.org/xmlns/quakeml/1.2"
    xmlns:bed="http://quakeml.org/xmlns/bed/1.2">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml"
        method="xml" />
    <xsl:template match="/q:quakeml/bed:eventParameters/bed:event">
        <metadata>
            <item title="Date/Time">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="bed:origin/bed:time/bed:value" />
                        <xsl:text> ± </xsl:text>
                        <xsl:value-of
                            select="format-number(bed:origin/bed:time/bed:uncertainty,
                            '0.00')" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Latitude (°)">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="bed:origin/bed:latitude/bed:value" />
                        <xsl:text> ± </xsl:text>
                        <xsl:value-of
                            select="format-number(bed:origin/bed:latitude/bed:uncertainty,
                            '0.00')" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Longitude (°)">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="bed:origin/bed:longitude/bed:value" />
                        <xsl:text> ± </xsl:text>
                        <xsl:value-of
                            select="format-number(bed:origin/bed:longitude/bed:uncertainty,
                            '0.00')" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Depth (km)">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="bed:origin/bed:depth/bed:value" />
                        <xsl:text> ± </xsl:text>
                        <xsl:value-of
                            select="format-number(bed:origin/bed:depth/bed:uncertainty,
                            '0.00')" />
                    </xsl:attribute>
                </text>
            </item>
        </metadata>
    </xsl:template>
</xsl:stylesheet>
