import unittest

import mock

from pulp_python.plugins import models, querysets

from .importers.test_sync import NUMPY_MANIFEST

_PACKAGES = [
    models.Package(
        name='nectar',
        packagetype='sdist',
        version='1.2.0',
        author='me',
        summary='does stuff',
        md5_digest='abcde',
        filename='nectar-1.2.0.tar.gz',
        _checksum='abcde',
        _checksum_type='made_up',
        path='some/url',
        _storage_path='/path/to/nectar-1.2.0.tar.gz'
    ),
    models.Package(
        name='nectar',
        packagetype='sdist',
        version='1.3.1',
        summary='does stuff',
        author='me',
        filename='nectar-1.3.1.tar.gz',
        md5_digest='fghij',
        _checksum='fghij',
        _checksum_type='made_up',
        path='some/url',
        _storage_path='/path/to/nectar-1.3.1.tar.gz'
    ),
    models.Package(
        name='pulp_python_plugins',
        packagetype='sdist',
        summary='does stuff',
        author='me',
        version='0.0.0',
        filename='pulp_python_plugins-0.0.0.tar.gz',
        md5_digest='klmno',
        _checksum='klmno',
        _checksum_type='made_up',
        path='some/url',
        _storage_path='/path/to/pulp_python_plugins-0.0.0.tar.gz'
    ),
]


class TestPythonPackageQuerySet(unittest.TestCase):

    @mock.patch('pulp_python.plugins.querysets.PythonPackageQuerySet.packages_in_repo')
    def test_packages_by_project(self, mock_pkg_qs):
        """
        Ensure that packages are grouped into a dictionary by project name.
        """
        mock_pkg_qs.return_value = _PACKAGES
        qs = querysets.PythonPackageQuerySet(mock.MagicMock(), mock.MagicMock())
        ret = qs.packages_by_project('mock_repo')
        self.assertTrue('nectar' in ret)
        self.assertEqual(ret['nectar'], _PACKAGES[0:2])
        self.assertTrue('pulp_python_plugins' in ret)
        self.assertEqual(ret['pulp_python_plugins'], [_PACKAGES[2]])

    def test_from_metadata(self):
        """
        Ensure that packages can be created from json metadata.
        """
        mock_doc = mock.MagicMock()
        qs = querysets.PythonPackageQuerySet(mock_doc, mock.MagicMock())
        qs.from_metadata(NUMPY_MANIFEST)
        # 1.9.1 has 5 units, 1.9.0 has 5, 1.8.0 has 2, 1.8.1 has 5, 1.8.2 has 5. Total should be 22.
        self.assertEqual(mock_doc.from_json.call_count, 22)
