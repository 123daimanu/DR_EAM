#import table
name<-"Pt_K_vrs_log(alpha)_wt.dat"   #weighted
#name<-"Pt_K_vrs_log(alpha).dat"    #unweighted
data<-read.table(name)


slope<-data$slope
err<-data$Delta_slope
k<-data$k
#pdf("slope_plot.pdf")			#unweighted
pdf("slope_plot_wt.pdf")    		#weighted
plot(k,slope,xlab="K",ylab="slope",main="Plot of K vrs Slope",ylim=c(.75,1.5))
arrows(k,slope-err,k,slope+err,length=0.05,angle=90,code=3)
abline(1,0,lwd=2)
#abline(v=1475,h=0,lty=4)
dev.off()
