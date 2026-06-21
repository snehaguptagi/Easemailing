const AboutSection = () => {
  return (
    <section className="py-20 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-8 text-foreground fade-in-up">
            What is AI Email Assistant?
          </h2>
        </div>
        
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="slide-in-left">
            <p className="text-lg leading-relaxed text-muted-foreground mb-6">
              Every email is a trigger—an intent to approve, assign, reply, route, or resolve.
              But most companies treat email as static noise.
            </p>
            <p className="text-lg leading-relaxed text-foreground mb-6 font-medium">
              AI Email Assistant changes that.
            </p>
            <p className="text-lg leading-relaxed text-muted-foreground mb-6">
              It's a Large Action Model for your inbox.
              It reads emails like a human, extracts key data, and kicks off workflows across your stack.
            </p>
            <p className="text-xl font-semibold text-foreground">
              Built for scale. Designed for operators.
            </p>
            <p className="text-lg text-muted-foreground mt-4">
              This isn't automation. This is operational intelligence.
            </p>
          </div>
          
          <div className="slide-in-right">
            <div className="bg-card rounded-xl p-8 shadow-lg">
              <div className="space-y-6">
                <div className="flex items-center space-x-4 fade-in-up stagger-1">
                  <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center">
                    <div className="w-6 h-6 bg-accent-foreground rounded"></div>
                  </div>
                  <span className="text-lg font-medium text-card-foreground">Automatically update your CRM</span>
                </div>
                
                <div className="flex items-center space-x-4 fade-in-up stagger-2">
                  <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center">
                    <div className="w-6 h-6 bg-accent-foreground rounded"></div>
                  </div>
                  <span className="text-lg font-medium text-card-foreground">Draft responses and internal alerts</span>
                </div>
                
                <div className="flex items-center space-x-4 fade-in-up stagger-3">
                  <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center">
                    <div className="w-6 h-6 bg-accent-foreground rounded"></div>
                  </div>
                  <span className="text-lg font-medium text-card-foreground">Assign tasks and launch approvals</span>
                </div>
                
                <div className="flex items-center space-x-4 fade-in-up stagger-4">
                  <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center">
                    <div className="w-6 h-6 bg-accent-foreground rounded"></div>
                  </div>
                  <span className="text-lg font-medium text-card-foreground">Escalate follow-ups when ignored</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;