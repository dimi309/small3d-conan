small3d conan package
=====================

Deployment
----------

In order to deploy the package locally, first deploy my variation of the
portaudio package to your local cache:

	git clone https://github.com/dimi309/portaudio-conan
	cd portaudio-conan
	conan export . --version=19.7.0

Then deploy the small3d package:

	git clone https://github.com/dimi309/small3d-conan
	cd small3d-conan
	conan export . --version=1.8016 (or master)
	
You can then use small3d as conan requirement `small3d/1.8016` or `small3d/master`


