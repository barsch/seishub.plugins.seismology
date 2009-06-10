<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml"
        method="xml" />
    <xsl:template match="/xseed/station_control_header/channel_identifier">
        <text>
            <xsl:attribute name="text">
                <xsl:if test="./location_identifier/text()">
                    <xsl:value-of select="location_identifier" />
                    <xsl:text> </xsl:text>
                </xsl:if>
                <xsl:value-of select="channel_identifier" />
            </xsl:attribute>
        </text>
    </xsl:template>
    <xsl:template
        match="/xseed/station_control_header/channel_identifier/channel_identifier">
        <text>
            <xsl:attribute name="text">
                <xsl:value-of select="current()" />
            </xsl:attribute>
        </text>
    </xsl:template>
    <xsl:template match="/xseed">
        <metadata>
            <item title="Station Name">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="station_control_header/station_identifier/site_name"
                         />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Station ID">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="station_control_header/station_identifier/station_call_letters"
                         />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Network ID">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="station_control_header/station_identifier/network_code"
                         />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Channel IDs">
                <xsl:apply-templates
                    select="/xseed/station_control_header/channel_identifier"
                 />
            </item>
            <item title="Latitude (°)">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="station_control_header/station_identifier/latitude"
                         />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Longitude (°)">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="station_control_header/station_identifier/longitude"
                         />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Elevation (m)">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="station_control_header/station_identifier/elevation"
                         />
                    </xsl:attribute>
                </text>
            </item>
            <xsl:if test="non_seed/station_images">
                <item title="Image">
                    <image>
                        <xsl:attribute name="src">
                            <xsl:value-of
                                select="non_seed/station_images/image" />
                        </xsl:attribute>
                    </image>
                </item>
            </xsl:if>
        </metadata>
    </xsl:template>
</xsl:stylesheet>
