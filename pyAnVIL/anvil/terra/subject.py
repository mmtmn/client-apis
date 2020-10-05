"""Client for reconciling terra subject."""

import logging
from attrdict import AttrDict


class Subject(object):
    """Represent terra subject."""

    def __init__(self, *args, workspace=None, samples=None):
        """Pass all args to AttrDict."""
        self.attributes = AttrDict(*args)
        self._logger = logging.getLogger(__name__)
        self.workspace_name = workspace.name
        self.schema = workspace.subject_schema
        self.sample_schema = workspace.sample_schema
        self.subject_property_name = workspace.subject_property_name
        self.namespace = workspace.attributes.workspace.namespace
        # find all samples associated with blobs
        self.samples = self._find_samples(samples)

    def __repr__(self):
        """Return attributes."""
        return str(self.attributes)

    @property
    def id(self):
        """Delegate to subclass."""
        raise Exception('Not implemented')

    def _find_samples(self, samples):
        """Get samples."""
        return samples[self.id]

    @property
    def missing_samples(self):
        """Test if no samples."""
        return len(self.samples) == 0

    @property
    def age(self):
        """Delegate to subclass."""
        raise Exception('Not implemented')

    @property
    def gender(self):
        """Deduce gender."""
        for p in ['gender', 'sex']:
            if p in self.attributes.attributes:
                gender = self.attributes.attributes[p]
                if gender in ['null', 'NA']:
                    return None
                return gender
        logging.getLogger(__name__).info(f"{self.workspace_name} {self.id} missing gender parameter")
        return None

    @property
    def ethnicity(self):
        """Deduce ethnicity."""
        for p in ['11-ancestry_detail,10-ancestry', 'ancestry', 'Race_Ethnicity', 'Ethnicity', 'RACE']:
            if p in self.attributes.attributes:
                ethnicity = self.attributes.attributes[p]
                if ethnicity in ['null', 'NA', '#N/A']:
                    return None
                if ethnicity in ['Hispanic or Latino', 'hispanic-or-latino', 'Hispanic', 'Hispanic/Latino', 'Puerto Rican']:
                    return 'hispanic'
                if ethnicity in ['African American', 'Black or African American']:
                    return 'black'
                if ethnicity in ['unknown', 'Unknown']:
                    return 'unknown'
                if ethnicity in ['White', 'Caucasian', 'Finnish']:
                    return 'white'
                if ethnicity in ['Not Hispanic or Latino', 'not-hispanic-or-latino', 'Non-Hispanic']:
                    return 'not-hispanic'
                if ethnicity in ['American Indian or Alaskan Native']:
                    return 'american-indian-or-alaskan-native'
                if ethnicity in ['not-asked', 'Not Asked']:
                    return 'not-asked'
                if ethnicity in ['Asian']:
                    return 'asian'
                return ethnicity
        logging.getLogger(__name__).info(f"{self.workspace_name} {self.id} missing ethnicity parameter")
        return None


class CCDGSubject(Subject):
    """Extend Subject class."""

    def __init__(self, *args, workspace=None, samples=None):
        """Call super."""
        super().__init__(*args, workspace=workspace, samples=samples)

    @property
    def id(self):
        """Deduce id."""
        return self.attributes.name

    @property
    def age(self):
        """Deduce age."""
        for p in ['Age', 'AGE', 'AGE_baseline']:
            if p in self.attributes.attributes:
                age = self.attributes.attributes[p]
                if not str(age).isnumeric():
                    logging.getLogger(__name__).warn(f"{self.workspace_name} {self.id} {p} not numeric")
                    return None
                return int(age)
        logging.getLogger(__name__).info(f"{self.workspace_name} {self.id} missing age parameter")
        return None


class CMGSubject(Subject):
    """Extend Subject class."""

    def __init__(self, *args, workspace=None, samples=None):
        """Call super."""
        super().__init__(*args, workspace=workspace, samples=samples)

    @property
    def id(self):
        """Deduce id."""
        return self.attributes.name

    @property
    def age(self):
        """Deduce age."""
        if '18-age_of_onset' not in self.attributes.attributes:
            logging.getLogger(__name__).info(f"{self.workspace_name} {self.id} missing 18-age_of_onset")
            return None
        age_of_onset = self.attributes.attributes['18-age_of_onset']
        if not str(age_of_onset).isnumeric():
            # logging.getLogger(__name__).warn(f"{self.workspace_name} {self.id} 18-age_of_onset not numeric {age_of_onset}")
            return None
        return int(age_of_onset)


class GTExSubject(Subject):
    """Extend Subject class."""

    def __init__(self, *args, workspace=None, samples=None):
        """Call super."""
        super().__init__(*args, workspace=workspace, samples=samples)

    @property
    def id(self):
        """Deduce id."""
        return self.attributes.name

    @property
    def age(self):
        """Deduce age."""
        if 'age' not in self.attributes.attributes:
            logging.getLogger(__name__).info(f"{self.workspace_name} {self.id} missing age")
            return None
        age = self.attributes.attributes['age']
        if not str(age).isnumeric():
            logging.getLogger(__name__).info(f"{self.workspace_name} {self.id} age not numeric")
            return None
        return int(age)


class ThousandGenomesSubject(Subject):
    """Extend Subject class."""

    def __init__(self, *args, workspace=None, samples=None):
        """Call super."""
        super().__init__(*args, workspace=workspace, samples=samples)

    @property
    def id(self):
        """Deduce id."""
        return self.attributes.name

    @property
    def age(self):
        """Deduce age."""
        return None


class eMERGESUbject(Subject):
    """Extend Subject class."""

    def __init__(self, *args, workspace=None, samples=None):
        """Call super."""
        super().__init__(*args, workspace=workspace, samples=samples)

    @property
    def id(self):
        """Deduce id."""
        return self.attributes.name

    @property
    def age(self):
        """Deduce age."""
        return None


def subject_factory(*args, **kwargs):
    """Return a specialized Subject class instance."""
    if 'CCDG' in kwargs['workspace'].name.upper():
        return CCDGSubject(*args, **kwargs)
    if 'CMG' in kwargs['workspace'].name.upper():
        return CMGSubject(*args, **kwargs)
    if 'GTEX' in kwargs['workspace'].name.upper():
        return GTExSubject(*args, **kwargs)
    if '1000G-HIGH-COVERAGE' in kwargs['workspace'].name.upper():
        return ThousandGenomesSubject(*args, **kwargs)
    if 'ANVIL_EMERGE' in kwargs['workspace'].name.upper():
        return eMERGESUbject(*args, **kwargs)
    raise Exception('Not implemented')
