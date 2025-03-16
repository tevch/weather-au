import weather_au

from datetime import datetime

# https://docs.python.org/3/library/xml.dom.html#module-xml.dom

class Observations:

    def __init__(self, state=None):

        self.state = state
        self.url = weather_au.OBSERVATION_PRODUCT_URL[state]
        self.soup = weather_au.fetch_xml(self.url)
        self.identifier = self.soup.identifier.contents[0]
        self.acknowedgment = f'Data courtesy of Bureau of Meteorology ({self.url})'
    

    def stations(self):
        # List of station attributes

        station_list =[]

        for station in self.soup.find_all('station'):
            station_list.append(station.attrs)

        return station_list


    def station_elements(self, wmo_id=None):
        # Element child tags for a specified station

        return self.soup.find('station', {'wmo-id': wmo_id})


    def station_attribute(self, wmo_id=None, attribute=None):

        attrs = self.soup.find('station', {'wmo-id': wmo_id}).attrs

        if attribute in attrs:
            return attrs[attribute]
        else:
            return None


    def period_attribute(self, wmo_id=None, attribute=None):

        elements = self.soup.find('station', {'wmo-id': wmo_id})

        attrs = elements.find('period').attrs

        if attribute in attrs:
            return attrs[attribute]
        else:
            return None


    def station_name(self, wmo_id=None):
        return self.station_attribute(wmo_id, 'stn-name')

    def site(self, wmo_id=None):
        return self.station_attribute(wmo_id, 'description')

    def lat(self, wmo_id=None):
        return self.station_attribute(wmo_id, 'lat')

    def lon(self, wmo_id=None):
        return self.station_attribute(wmo_id, 'lon')

    def temp_c(self, wmo_id=None):
        return self.station_el_value(wmo_id, 'element', 'type', 'air_temperature')

    def dewpoint_c(self, wmo_id=None):
        return self.station_el_value(wmo_id, 'element', 'type', 'dew_point')

    def altim_in_hg(self, wmo_id=None):
        return self.station_el_value(wmo_id, 'element', 'type', 'pres')


    def observation_time(self, wmo_id=None):
        observation_time_str = self.station_el_value(wmo_id, 'period', 'time-utc', None)
        utc_time = datetime.strptime(observation_time_str, "%Y-%m-%dT%H:%M:%S+00:00")
        observation_time_str_utc = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        return observation_time_str_utc

    def wind_speed_kt(self, wmo_id=None):
        return self.station_el_value(wmo_id, 'element', 'type', 'wind_spd')

    def wind_dir_degrees(self, wmo_id=None):
        return self.station_el_value(wmo_id, 'element', 'type', 'wind_dir_deg')

    def wind_gust_kt(self, wmo_id=None):
        return self.station_el_value(wmo_id, 'element', 'type', 'wind_gust_spd')

    def station_el_value(self, wmo_id=None, tag=None, attr=None, attr_name=None):
        """ Don't assume that any elements exist or that there is an element with type air_temperature
        """

        elements = self.soup.find('station', {'wmo-id': wmo_id})

        if elements is not None:
            if attr_name:
                el = elements.find(tag, {attr: attr_name})
                if el is not None and len(el.contents) > 0:
                    return str(el.contents[0])
            else:
                el = elements.find(tag)
                if el.has_attr(attr):
                    return el[attr]



        return None


    def rainfall(self, wmo_id=None):
        """ Don't assume that any elements exist or that there is an element with type rainfall
        """

        elements = self.soup.find('station', {'wmo-id': wmo_id})

        if elements is not None:
            rainfall_el = elements.find('element', {'type': 'rainfall'})

            if rainfall_el is not None and len(rainfall_el.contents) > 0:
                    return rainfall_el.contents[0]

        return None

    def __str__(self):
        return str(self.soup)
