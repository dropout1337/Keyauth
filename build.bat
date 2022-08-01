@echo off

echo building..
python .\setup.py bdist bdist_wheel

echo uploading
twine upload --skip-existing dist/*