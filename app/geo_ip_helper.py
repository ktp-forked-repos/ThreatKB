import geoip2.database
import os
import pyzipcode

from ipaddr import IPAddress
from app import app
from app.models import cfg_settings

app.config["GEOIP_ASN_DATABASE_FILE"] = cfg_settings.Cfg_settings.get_private_setting("GEOIP_ASN_DATABASE_FILE")
if not app.config["GEOIP_ASN_DATABASE_FILE"]:
    app.config["GEOIP_ASN_DATABASE_FILE"] = os.getenv('GEOIP_ASN_DATABASE_FILE',
                                                      '/usr/local/ThreatKB/MaxMind/GeoLite2-ASN.mmdb')

app.config["GEOIP_CITY_DATABASE_FILE"] = cfg_settings.Cfg_settings.get_private_setting("GEOIP_CITY_DATABASE_FILE")
if not app.config["GEOIP_CITY_DATABASE_FILE"]:
    app.config["GEOIP_CITY_DATABASE_FILE"] = os.getenv('GEOIP_CITY_DATABASE_FILE',
                                                       '/usr/local/ThreatKB/MaxMind/GeoLite2-City.mmdb')

GEOIP_ASN_DATABASE_FILE = app.config["GEOIP_ASN_DATABASE_FILE"]
GEOIP_CITY_DATABASE_FILE = app.config["GEOIP_CITY_DATABASE_FILE"]
ASN_READER = geoip2.database.Reader(GEOIP_ASN_DATABASE_FILE)
CITY_READER = geoip2.database.Reader(GEOIP_CITY_DATABASE_FILE)
ZIPCODE_DB = pyzipcode.ZipCodeDatabase()


def get_geo_for_ip(ip_address):
    try:
        ip_address = IPAddress(ip_address)
        if not ip_address.is_private:
            asn_info = ASN_READER.asn(ip_address)
            city_info = CITY_READER.city(ip_address)
            zip_code = city_info.postal.code
            return dict(
                ip=ip_address,
                asn=asn_info.autonomous_system_organization,
                country_code=city_info.country.iso_code,
                city=city_info.city.names["en"],
                state=ZIPCODE_DB[zip_code].state,
                zip_code=zip_code,
                country=city_info.country.names["en"],
                continent=city_info.continent.names["en"]
            )
        return None
    except Exception as e:
        return None
