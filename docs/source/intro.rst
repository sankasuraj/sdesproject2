


################
What is Kriging?
################

In statistics, originally in geostatistics, Kriging or Gaussian process regression is a method of interpolation for which the interpolated values are modeled by a Gaussian process governed by prior covariances, as opposed to a piecewise-polynomial spline chosen to optimize smoothness of the fitted values. Under suitable assumptions on the priors, Kriging gives the best linear unbiased prediction of the intermediate values. Interpolating methods based on other criteria such as smoothness need not yield the most likely intermediate values. The method is widely used in the domain of spatial analysis and computer experiments. The technique is also known as Wiener–Kolmogorov prediction, after Norbert Wiener and Andrey Kolmogorov.


#################
Where it is used?
#################

Although Kriging was developed originally for applications in geostatistics, it is a general method of statistical interpolation that can be applied within any discipline to sampled data from random fields that satisfy the appropriate mathematical assumptions.

To date Kriging has been used in a variety of disciplines, including the following:

*   Environmental Science
*   Hydrogeology
*   Mining
*   Real State appraisal
*   Remote sensing
*   Natural resources


###########
Methodology
###########

* The data is read from the input file.
* The data is divided in the ratio 4:1 where the majority is used for training while the remaining is used for error estimation.
* Now, the model is prepared using the full data.

