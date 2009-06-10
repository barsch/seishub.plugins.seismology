<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml"
        method="xml" />
    <xsl:template match="/event">
        <metadata>
            <item title="Date/Time">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="origin/time/value" />
                        <xsl:text> ± </xsl:text>
                        <xsl:value-of
                            select="format-number(origin/time/uncertainty,
                            '0.00')" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Latitude (°)">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="origin/latitude/value" />
                        <xsl:text> ± </xsl:text>
                        <xsl:value-of
                            select="format-number(origin/latitude/uncertainty,
                            '0.00')" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Longitude (°)">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="origin/longitude/value" />
                        <xsl:text> ± </xsl:text>
                        <xsl:value-of
                            select="format-number(origin/longitude/uncertainty,
                            '0.00')" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Depth (km)">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                        select="origin/depth/value" />
                        <xsl:text> ± </xsl:text>
                        <xsl:value-of
                            select="format-number(origin/depth/uncertainty,
                            '0.00')" />
                    </xsl:attribute>
                </text>
            </item>
        </metadata>
    </xsl:template>
</xsl:stylesheet>
