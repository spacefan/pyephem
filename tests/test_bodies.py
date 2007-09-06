#!/usr/bin/env python

import sys
from sets import Set
from ephem_test import *

# The attributes which each class of object should support (these
# lists are used by several of the functions below).

satellite_attributes = ('sublat', 'sublong', 'elevation',
                        'range', 'range_velocity', 'eclipsed')

attribute_list = (
    (Body, False,
     ('ra', 'dec', 'elong', 'mag', 'size')),
    (Body, True,
     ('az', 'alt', 'circumpolar', 'neverup', 'rise_time', 'rise_az',
      'transit_time', 'transit_alt', 'set_time', 'set_az')),
    (Planet, False,
     ('hlong', 'hlat', 'sun_distance', 'earth_distance', 'phase')),
    (Moon, False,
     ('colong', 'subsolar_lat', 'libration_lat', 'libration_long')),
    (Saturn, False,
     ('earth_tilt', 'sun_tilt')),
    (PlanetMoon, False,
     ('ra', 'dec', 'x', 'y', 'z', 'earth_visible', 'sun_visible')),
    (PlanetMoon, True,
     ('az', 'alt')),
    )

# Return a dictionary whose keys are all known body attributes,
# and whose values are the exceptions we expect to receive for
# trying to access each attribute from the given body, or the
# value True for attributes which should not raise exceptions.

def predict_attributes(body, was_computed, was_given_observer):
    predictions = {}
    for bodytype, needs_observer, attrs in attribute_list:
        for attr in attrs:
            if attr in predictions and predictions[attr] != AttributeError:
                continue
            if not isinstance(body, bodytype):
                predictions[attr] = AttributeError
            elif not was_computed:
                predictions[attr] = RuntimeError
            elif needs_observer and not was_given_observer:
                predictions[attr] = RuntimeError
            else:
                predictions[attr] = None
    return predictions

# Determine whether each kind of body supports the set of attributes
# we believe it should.

class body_suite(MyTestCase):
    def setUp(self):
        self.date = date('1955/05/21')

        self.obs = obs = Observer()
        obs.lat, obs.long, obs.elev = '33:45:10', '-84:23:37', 320.0
        obs.date = '1997/2/15'

    # Try accessing each attribute in attribute_list from the given
    # body, recording the exceptions we receive in a dictionary, and
    # storing True for attributes whose access raises no exception.

    def measure_attributes(self, body):
        attributes = {}
        for bodytype, needs_observer, attrs in attribute_list:
            for attr in attrs:
                try:
                    getattr(body, attr)
                except:
                    attributes[attr] = sys.exc_info()[1]
                else:
                    attributes[attr] = None
        return attributes

    # Use the above functions to predict which attributes of the given
    # body should be accessible, and then test to see whether the
    # reality matches our prediction.

    def compare_attributes(self, body, was_computed, was_given_observer):
        p = predict_attributes(body, was_computed, was_given_observer)
        t = self.measure_attributes(body)
        for a in Set(p).union(t):
            if p[a] is None and t[a] is None:
                continue
            if p[a] and isinstance(t[a], p[a]):
                continue
            if was_computed:
                if was_given_observer:
                    adjective = 'topo'
                else:
                    adjective = 'geo'
                adjective += 'centrically computed'
            else:
                adjective = 'uncomputed'
            raise TestError('accessing %s of %s %s '
                            'raised %r "%s" instead of %r'
                            % (a, adjective, body,
                               t[a], t[a].args[0], p[a]))

    # Run the body - which should not yet have been compute()d when
    # first given to us - through several computations to determine
    # whether its attributes become available when we think they
    # should.

    def run_body(self, body):
        self.compare_attributes(body, False, False)
        body.compute()
        self.compare_attributes(body, True, False)
        body.compute(self.obs)
        self.compare_attributes(body, True, True)
        body.compute()
        self.compare_attributes(body, True, False)

    def test_Named(self):
        for named_object in (Mercury, Venus, Mars, Jupiter, Saturn,
                             Uranus, Neptune, Pluto, Sun, Moon,
                             Phobos, Deimos,
                             Io, Europa, Ganymede, Callisto,
                             Mimas, Enceladus, Tethys, Dione, Rhea,
                             Titan, Hyperion, Iapetus, Ariel, Umbriel,
                             Titania, Oberon, Miranda):
            self.run_body(named_object())

    # For each flavor of user-definable body, 

    def build(self, bodytype, dbentry, attributes):

        # Build one body from the Ephem-formatted entry.

        if isinstance(dbentry, tuple):
            bl = readtle(*dbentry)
        else:
            bl = readdb(dbentry)

        # Build another body by setting the attributes on a body.

        ba = bodytype()
        for attribute, value in attributes.iteritems():
            try:
                setattr(ba, attribute, value)
            except TypeError:
                raise TestError, ('cannot modify attribute %s of %r: %s'
                                  % (attribute, ba, sys.exc_info()[1]))
        if not isinstance(bl, bodytype):
            raise TestError, ('ephem database entry returned type %s'
                              ' rather than type %s' % (type(bl), bodytype))

        # Now, compare the bodies to see if they are equivalent.
        # First test whether they present the right attributes.

        self.run_body(bl), self.run_body(ba)

        # Check whether they appear in the same positions.

        for circumstance in self.date, self.obs:
            is_observer = isinstance(circumstance, Observer)
            bl.compute(circumstance), ba.compute(circumstance)
            attrs = [ a for (a,e)
                      in predict_attributes(bl, 1, is_observer).items()
                      if not e ]
            for attr in attrs:
                vl, va = getattr(bl, attr), getattr(ba, attr)
                if isinstance(vl, float):
                    vl, va = str(float(vl)), str(float(va))
                if vl != va:
                    raise TestError, ("%s item from line returns %s for %s"
                                      " but constructed object returns %s"
                                      % (type(bl), vl, attr, va))

    def test_FixedBody(self):
        self.build(
            bodytype=FixedBody,
            dbentry='Achernar,f|V|B3,1:37:42.9,-57:14:12,0.46,2000',
            attributes={'name': 'Achernar',
                        '_ra': '1:37:42.9', '_dec': '-57:14:12',
                        'mag': 0.46, '_epoch': '2000',
                        })

    def test_EllipticalBody(self):
        self.build(
            bodytype=EllipticalBody,
            dbentry=('C/1995 O1 (Hale-Bopp),e,89.3918,282.4192,130.8382,'
                     '186.4302,0.0003872,0.99500880,0.0000,'
                     '03/30.4376/1997,2000,g -2.0,4.0'),
            attributes={'name': 'Hale-Bopp', '_inc': 89.3918,
                        '_Om': 282.4192, '_om': 130.8382,
                        '_a': 186.4302, '_e': 0.99500880, '_M': 0.0000,
                        '_epoch_M': '1997/03/30.4376', '_epoch': '2000',
                        '_size': 0, '_g': -2.0, '_k': 4.0,
                        })

    def test_HyperbolicBody(self):
        self.build(
            bodytype=HyperbolicBody,
            dbentry=('C/1999 J2 (Skiff),h,04/05.7769/2000,86.3277,50.0353,'
                     '127.1286,1.002879,7.110858,2000,2.0,4.0'),
            attributes = {'name': 'Skiff', '_epoch_p': '2000/4/5.7769',
                          '_inc': 86.3277, '_Om': 50.0353, '_om': 127.1286,
                          '_e': 1.002879, '_q': 7.110858, '_epoch': '2000',
                          '_g': 2.0, '_k': 4.0,
                          })

    def test_ParabolicBody(self):
        self.build(
            bodytype=ParabolicBody,
            dbentry=('C/2004 S1 (Van Ness),p,12/08.9212/2004,114.6676,'
                     '92.8155,0.681783,19.2198,2000,16.5,4.0'),
            attributes={'name': 'Van Ness', '_epoch_p': '2004/12/8.9212',
                        '_inc': 114.6676, '_om': 92.8155, '_q': 0.681783,
                        '_Om': 19.2198, '_epoch': '2000',
                        '_g': 16.5, '_k': 4.0
                        })

    def test_EarthSatellite(self):
        self.build(
            bodytype=EarthSatellite,
            dbentry=('HST                     ',
                     '1 20580U 90037B   04296.45910607  .00000912 '
                     ' 00000-0  59688-4 0  1902',
                     '2 20580  28.4694  17.3953 0004117 265.2946  '
                     '94.7172 14.99359833594524'),
            attributes={'name': 'Hubble Telescope',
                        '_epoch': date('2004') + 296.45910607 - 1,
                        '_decay': .00000912, '_drag': .59688e-4,
                        '_inc': 28.4694, '_raan': 17.3953,
                        '_e': 4117e-7, '_ap': 265.2946, '_M': 94.7172,
                        '_n': 14.99359833, '_orbit': 59452,
                        })

# Make sure the constellation function forces objects to determine
# their position before using their right ascension and declination.

class function_suite(unittest.TestCase):
    def test_constellation(self):
        oneb = readdb('Orion Nebula,f,5.59,-5.45,2,2000.0,')
        oneb.compute('1999/2/28')
        self.assertEqual(constellation(oneb), ('Ori', 'Orion'))

#

class riset(MyTestCase):
    def setUp(self):
        self.obs = obs = Observer()
        obs.lat, obs.long, obs.elev = '33:45:10', '-84:23:37', 320.0
        obs.date = '1997/2/15'

        self.polaris = readdb('Polaris,f|M|F7,2:31:48.704,89:15:50.72,2.02,2000')
        self.rigel = readdb('Rigel,f|M|B8,5:14:32.3,-8:12:6,0.12,2000')

if __name__ == '__main__':
    unittest.main()
