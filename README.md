## This repository holds a conan recipe for Abseil.

[![Build status](https://ci.appveyor.com/api/projects/status/qw26b3cm4l60g29q/branch/testing/git-master?svg=true)](https://ci.appveyor.com/project/BinCrafters/conan-abseil/branch/testing/git-master)
[![Build Status](https://travis-ci.org/bincrafters/conan-abseil.svg?branch=testing%2Fgit-master)](https://travis-ci.org/bincrafters/conan-abseil)

[Conan.io](https://conan.io) package for [Abseil](https://github.com/abseil/abseil-cpp) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/bincrafters/public-conan/Abseil%3Abincrafters).

## For Users: Use this package

### Custom Package Options

This package has the following custom package options: 

|Option Name	| Default Value   | Possible Value    
|-----------------|------------------|------------------
|with_bazel       | True               | True/False              

`with_bazel` - The current default of true assumes you do not have Bazel installed, and so this package will include the bincrafters package for Bazel as a dependency. Thus, Bazel will be downloaded and installed automatically.  This can add significant convenience in many cases.  However, this will obviously take additional time to download which is slightly inefficient if you already have Bazel installed.  If this option is set to `False` a binary called `bazel` must be available at the CLI (typically via the PATH environment variable).  Conan options can be set in multiple places such as *conanfile.txt* and *conanfile.py*, or passed at the CLI when running `conan install ..` for example:  

    $ conan install Abseil/latest@bincrafters/testing -o Abseil:with_bazel=False
	
Of note, the bincrafters Bazel package has it's own option for including an embedded JDK, or using one already installed.  Here's an example of installing Abseil with the default option to include Bazel, but to tell Bazel not to include the embedded JDK. 
	
    $ conan install Abseil/latest@bincrafters/testing -o bazel_installer:with_jdk=False

Also of note, the Bazel package currently only supports x64 architecture.  If you want to use this package on a different architecture, you must have your own Bazel installation, and then set the `with_bazel` to `False` as shown above.
	
### Conan "latest" version convention

Abseil has a unique versioning philosophy, so this package offers a unique versioning option on the packages by using a "conan alias" named "latest". 

["Conan Alias feature Explained"](http://conanio.readthedocs.io/en/latest/reference/commands/alias.html?highlight=conan%20alias)

In summary, if users want to follow the Abseil philosophy of "Live At Head" as closely as possible while getting the benefits of using Conan, they can reference the version of "latest" in their requirements as shown in the example below.  "latest" is just an alias which redirects to an actual version of an Abseil package. Bincrafters will compile, create and upload binaries for the package on some recurring basis, and "latest" will regularly be updated to point to the most recent one.  Of note, because Abseil does not use semantic versioning, a datestamp will be used as the version number on the concrete Bincrafters packages and the `source()` method of each version of the recipe will point to the most recent commit of Abseil available at the time that package version was created.  Currently, there is only a "master" branch for Abseil. 

The result of using "latest" is that whenever Bincrafters uploads a new version of the recipe and updates the alias, your next call to "conan install" will download (or build if necessary), and the immediately begin using the latest version of Abseil. 

If users want to use Abseil, perhaps staying up to date but with slightly more control over when the updates happen, they can choose to point to the concrete packages. Pointing to concrete packages by date has many other uses, such as going back to a specific point in time for troubleshooting. 

### Basic setup

    $ conan install Abseil/latest@bincrafters/testing

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    Abseil/latest@bincrafters/testing

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..
	
Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git. 

## For Packagers: Publish this Package

The example below shows the commands used to publish to bincrafters conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly. 

## Build and package 

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from `build_requires` and `requires` , and then running the `build()` method. 

    $ conan create bincrafters/testing
	
## Add Remote

	$ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"

## Upload

To upload a package with an alias involved, it's a three-step process. 

The first step is standard, upload the concrete package you've recently built:

    $ conan upload Abseil/20171004@bincrafters/testing --all -r bincrafters

The second step is to update the "alias package": 

	$ conan alias Abseil/latest@bincrafters/testing Abseil/20171004@bincrafters/testing

The third step is to upload the alias package:

	$conan upload Abseil/latest@bincrafters/testing --all -r bincrafters
	
### License
[Apache License 2.0](LICENSE)
