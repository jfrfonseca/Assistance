for (( i=0;i<10;i++ )); do

	echo "Run $i"

	time -p java -cp weka.jar weka.classifiers.functions.SMO       -t data/breast-cancer.arff -x 10   >  outputs/$i-SMO-breast-cancer.arff-output.dat
	time -p java -cp weka.jar weka.classifiers.functions.SMO       -t data/labor.arff -x 10    >  outputs/$i-SMO-labor.arff-output.dat

	time -p java -cp weka.jar weka.classifiers.trees.J48           -t data/weather.numeric.arff -x 10 >  outputs/$i-J48-weather.numeric.arff-output.dat
	time -p java -cp weka.jar weka.classifiers.trees.J48           -t data/weather.nominal.arff -x 10 >  outputs/$i-J48-weather.nominal.arff-output.dat

	time -p java -cp weka.jar weka.classifiers.trees.DecisionStump -t data/cpu.with.vendor.arff -x 10 >  outputs/$i-DCS-cpu.with.vendor.arff-output.dat
	time -p java -cp weka.jar weka.classifiers.trees.DecisionStump -t data/cpu.arff -x 10      >  outputs/$i-DCS-cpu.arff-output.dat

	time -p java -cp weka.jar weka.classifiers.meta.AdaBoostM1     -t data/breast-cancer.arff -x 10   >  outputs/$i-AB1-breast-cancer.arff-output.dat
	time -p java -cp weka.jar weka.classifiers.meta.AdaBoostM1     -t data/labor.arff -x 10    >  outputs/$i-AB1-labor.arff-output.dat

	time -p java -cp weka.jar weka.classifiers.bayes.NaiveBayes    -t data/credit-g.arff -x 10 >  outputs/$i-NBY-credit-g.arff-output.dat
	time -p java -cp weka.jar weka.classifiers.bayes.NaiveBayes    -t data/iris.2D.arff -x 10  >  outputs/$i-NBY-iris.2D.arff-output.dat

	time -p java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -t data/credit-g.arff -x 10 >  outputs/$i-MLP-credit-g.arff-output.dat
	time -p java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -t data/iris.2D.arff -x 10  >  outputs/$i-MLP-iris.2D.arff-output.dat

done
