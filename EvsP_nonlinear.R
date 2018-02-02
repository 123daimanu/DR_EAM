Theoretical_alpha=3.4383e-37 #col m
intersection=1475
fileName<-c("Pt_test_Sept19_E1_PzVrK.dat","Pt_test_Sept19_E2_PzVrK.dat","Pt_test_Sept19_E3_PzVrK.dat","Pt_test_Sept19_E8_PzVrK.dat","Pt_test_Sept19_E4_PzVrK.dat","Pt_test_Sept19_E5_PzVrK.dat","Pt_test_Sept19_E6_PzVrK.dat","Pt_test_Sept19_E7_PzVrK.dat")
Ef<-10**(-8)+0.125*seq(1,8)
E<-Ef*10^10
print(Ef)
n=length(fileName)
pz<-matrix(seq(1,8*17),nrow=8,ncol=17)
err<-matrix(seq(1,8*17),nrow=8,ncol=17)
for(j in seq(1,17)){
	for( i in seq(1,8)){
		data<-read.table(fileName[i])
		pz[i,j]<-data$V2[j]
		err[i,j]<-abs(data$V3[j])

	
	}
}
count<-1:17
k<-1:17
alpha<-1:17
hyper_alpha<-1:17
ealpha<-1:17
ehyper_alpha<-1:17
for (var in count){


	#file<-paste(as.character((var+1)*100),"k_nonlinear.pdf") #unweighted
	file<-paste(as.character((var+1)*100),"k_nonlinear_W_many_equal.pdf")    #weighted
	p<-pz[,var]
	
	er<-err[,var]
	nonlinear_func<-formula(p~a*Ef+b*Ef^3)
	ds<-data.frame(Ef=Ef,p=p)
	fit<-nls(nonlinear_func,data=ds,start=list(a=10^(-26),b=0),trace=F)					#unweighted
	#fit<-nsl(p~a*E+b*E^2,weights=1/er)				#weighted fit where weight is 1/err
	summ<-summary(fit)
	alpha[var]<-(summ$coef[1,1])
	hyper_alpha[var]<-(summ$coef[2,1])
	ealpha[var]<-(summ$coef[1,2])
	ehyper_alpha[var]<-(summ$coef[2,2])
	pdf(file)

	plot(E,p,main=paste("k = ",as.character((var+1)*100)),xlab=expression(E),ylab=expression(p_z))
	lines(E,predict(fit),lty=2,col="red",lwd=3)
	arrows(E, p-er, E, p+er, length=0.05, angle=90, code=3)
	dev.off()

}
k<-(k+1)*100
fit<-smooth.spline(k,alpha,all.knots=T)

#pdf("best_alpha_nonlinear.pdf")			#unweighted
pdf("best_alpha_wt_nonliner_many_equal.pdf")			#weighted


plot(k,alpha,xlab="K",ylab=expression(alpha),main="K vrs alpha for Pt100")
lines(fit,lty=3)
arrows(k,alpha-ealpha,k,alpha+ealpha,length=0.05,angle=90,code=3)
abline(Theoretical_alpha,0,lwd=2)
dev.off()


#pdf("hyper_alpha_plot_nonlinear.pdf")			#unweighted
pdf("hyper_alpha_plot_wt_nonlinear_many_equal.pdf")	    		#weighted
plot(k,hyper_alpha,xlab="K",ylab=expression(hyper_alpha),main="Plot of K vrs hyper_alpha ")
arrows(k,hyper_alpha-ehyper_alpha,k,hyper_alpha+ehyper_alpha,length=0.05,angle=90,code=3)

dev.off()

dataTable<-list("k"=k,"alpha"=alpha,"Delta_alpha"=ealpha,"hyper_alpha"=hyper_alpha,"Delta_hyper_alpha"=ehyper_alpha)

#write.table(dataTable,"Pt_K_vrs_alpha_halpha.dat")	#unweighted
write.table(dataTable,"Pt_K_vrs_alpha_halpha_wt_many_equal.dat")   #weighted
