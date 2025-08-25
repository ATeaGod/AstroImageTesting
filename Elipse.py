import numpy as np
import matplotlib.pyplot as plt
from photutils.aperture import EllipticalAperture
from astropy.io import fits
from astropy.utils.data import download_file
from photutils.isophote import Ellipse, build_ellipse_model

# Display Graphs During Creation #

DispGraph = True
ginput = input("Would You Like To Display Graphs (y/n) ")
if ginput == "y":
    DispGraph = True
if ginput == "n":
    DispGraph = False

# file stuffs #

filepath = input("FilePath >>> ")
hdu = fits.open(filepath)
data = hdu[0].data
hdu.close()

# Elipse Creation #

ellipse = Ellipse(data)
isolist = ellipse.fit_image(sma0=20.)
print(isolist.to_table())

# Brightness Graph #
if DispGraph == True:
    plt.figure(figsize=(8, 4))
    plt.scatter(isolist.sma**0.25, -2.5*np.log10(isolist.intens))
    plt.title("brightness profile")
    plt.xlabel('sma**1/4')
    plt.ylabel('Brightness')
    plt.gca().invert_yaxis()
    plt.show()

# Something #
if DispGraph == True:
    plt.figure(figsize=(10, 5))
    plt.figure(1)

    plt.subplot(221)
    plt.errorbar(isolist.sma, isolist.eps, yerr=isolist.ellip_err, fmt='o', markersize=4)
    plt.xlabel('Semimajor axis length')
    plt.ylabel('Ellipticity')

    plt.subplot(222)
    plt.errorbar(isolist.sma, isolist.pa/np.pi*180., yerr=isolist.pa_err/np.pi* 80., fmt='o', markersize=4)
    plt.xlabel('Semimajor axis length')
    plt.ylabel('PA (deg)')

    plt.subplot(223)
    plt.errorbar(isolist.sma, isolist.x0, yerr=isolist.x0_err, fmt='o', markersize=4)
    plt.xlabel('Semimajor axis length')
    plt.ylabel('X0')

    plt.subplot(224)
    plt.errorbar(isolist.sma, isolist.y0, yerr=isolist.y0_err, fmt='o', markersize=4)
    plt.xlabel('Semimajor axis length')
    plt.ylabel('Y0')

    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.35, wspace=0.35)
    plt.show()

# Model Generation #

model_image = build_ellipse_model(data.shape, isolist)

residual = data - model_image

# Final Graph Creation #

figure, axis = plt.subplots(1, 3)
axis[0].imshow(data, origin='lower')
axis[0].set_title("Galaxy")
axis[1].imshow(model_image, origin='lower')
axis[1].set_title("Galaxy Model")
axis[2].imshow(residual, origin='lower')
axis[2].set_title("Residual Image")
plt.show()

# File Saving #

hdu_residual = fits.PrimaryHDU(residual)
hdu_residual.writeto('residual.fits', overwrite=True)
hdu_model = fits.PrimaryHDU(model_image)
hdu_model.writeto('model_image.fits', overwrite=True)
