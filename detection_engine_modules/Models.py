# init
#	self.model_dir
#	self.models (array of de-serialised model objects)

# del

# load_models(self) (de-serialise (de-pickle) the models from the directory)

# predict(self, flow)
#	for model in self.models:
#		prediction = predict(flow)
#   	flow = flow.append(prediction)
#	
#	return flow
