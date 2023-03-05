small3d conan package
=====================

Deployment
----------

In order to deploy the package locally, first deploy my variation of the
portaudio package to your local cache:

	git clone https://github.com/dimi309/portaudio-conan
	cd portaudio-conan
	conan export . --version=19.7.0
	
If you would like to use Vulkan, you will also need my variation of the
vulkan-loader package (this is temporary until the conan center index
verion gets fixed - it has a small bug):

	git clone https://github.com/dimi309/vulkan-loader-conan
	cd vulkan-loader-conan
	conan export . --version=1.3.239.0

Then deploy the small3d package:

	git clone https://github.com/dimi309/small3d-conan
	cd small3d-conan
	conan export .
	
You can then use small3d as conan requirement `small3d/master`
