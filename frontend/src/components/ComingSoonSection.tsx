const ComingSoonSection = () => {
  const features = [
    {
      module: "Category Config",
      title: "Design how AI Email Assistant thinks.",
      description: "Define your own logic for classifying emails by use case or team. Make AI Email Assistant uniquely aware of what matters to your org.",
      benefits: [
        "No generic AI guesses.",
        "Every team—from Sales to Finance—gets tailored intent recognition."
      ]
    },
    {
      module: "Integration Hub",
      title: "Plug into your tools. No friction.",
      description: "Connect AI Email Assistant to Slack, Teams, Notion, HubSpot, Zoho, ClickUp, and more.",
      benefits: [
        "Stay where your team works.",
        "Get updates and trigger actions without switching platforms."
      ]
    },
    {
      module: "Routing Rules",
      title: "Emails → Tasks → The Right Person",
      description: "Build logic that automatically assigns or escalates based on: Keywords and intent, Sender or domain, Attachments or timing",
      benefits: [
        "Never lose time forwarding, chasing, or triaging emails again.",
        "AI Email Assistant handles it before anyone asks."
      ]
    },
    {
      module: "Action Dashboard",
      title: "Track it all. In real time.",
      description: "See what's been extracted, triggered, routed, or delayed—team by team, thread by thread.",
      benefits: [
        "Full transparency.",
        "No more guessing what happened after someone said \"Noted.\""
      ]
    }
  ];

  const bonusModule = {
    module: "Memory Layer",
    title: "Train AI Email Assistant over time to recognize recurring clients, team habits, and your org's language.",
    benefits: [
      "Gets smarter the more you use it.",
      "Understands your internal lingo and patterns."
    ]
  };

  return (
    <section className="py-20 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-20">
          <h2 className="text-5xl md:text-6xl font-bold mb-8 text-foreground fade-in-up">
            Coming Soon — Your Command Center for Email-Driven Ops
          </h2>
          <p className="text-xl text-muted-foreground fade-in-up stagger-1 max-w-4xl mx-auto">
            These upcoming modules will give you full control over how your organization works, straight from the inbox.
          </p>
        </div>
        
        <div className="space-y-16">
          {features.map((feature, index) => (
            <div key={index} className={`fade-in-up stagger-${index + 1}`}>
              <div className={`flex flex-col lg:flex-row items-center gap-12 ${index % 2 === 1 ? 'lg:flex-row-reverse' : ''}`}>
                {/* Feature Card */}
                <div className="lg:w-2/3">
                  <div className="bg-card rounded-2xl p-8 shadow-xl border border-border/20 hover:shadow-2xl transition-all duration-300 hover:scale-105">
                    <div className="flex items-start space-x-6">
                      <div className="w-20 h-20 bg-gradient-to-br from-primary to-primary/70 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg">
                        <div className="w-10 h-10 bg-primary-foreground rounded-lg"></div>
                      </div>
                      <div className="flex-1">
                        <h3 className="text-3xl font-bold text-card-foreground mb-3">
                          {feature.module}
                        </h3>
                        <h4 className="text-xl font-medium text-primary mb-4">
                          {feature.title}
                        </h4>
                        <p className="text-muted-foreground leading-relaxed text-lg mb-6">
                          {feature.description}
                        </p>
                        <div className="space-y-3">
                          <p className="text-base font-semibold text-card-foreground">Why it matters:</p>
                          {feature.benefits.map((benefit, benefitIndex) => (
                            <div key={benefitIndex} className="flex items-start bg-background/50 rounded-lg p-3">
                              <span className="text-primary mr-3 text-lg font-bold">→</span>
                              <p className="text-muted-foreground">{benefit}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Visual Element */}
                <div className="lg:w-1/3">
                  <div className="relative">
                    <div className="w-full h-64 bg-gradient-to-br from-accent/20 to-accent/10 rounded-2xl flex items-center justify-center border border-accent/30">
                      <div className="text-center">
                        <div className="w-24 h-24 bg-accent rounded-full mx-auto mb-4 flex items-center justify-center">
                          <div className="w-12 h-12 bg-accent-foreground rounded-full"></div>
                        </div>
                      </div>
                    </div>
                    {/* Floating elements */}
                    <div className="absolute -top-4 -right-4 w-8 h-8 bg-primary rounded-full animate-pulse"></div>
                    <div className="absolute -bottom-4 -left-4 w-6 h-6 bg-secondary rounded-full animate-pulse delay-700"></div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {/* Bonus Module - Special Layout */}
        <div className="mt-20">
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold text-primary mb-2 fade-in-up stagger-5">Bonus Module (Optional)</h3>
            <div className="w-24 h-1 bg-gradient-to-r from-primary to-secondary mx-auto"></div>
          </div>
          
          <div className="bg-gradient-to-r from-card to-card/80 rounded-3xl p-10 shadow-2xl border border-primary/20 fade-in-up stagger-6">
            <div className="flex flex-col lg:flex-row items-center gap-8">
              <div className="lg:w-1/4">
                <div className="w-32 h-32 bg-gradient-to-br from-secondary to-secondary/70 rounded-full flex items-center justify-center mx-auto shadow-xl">
                  <div className="w-16 h-16 bg-secondary-foreground rounded-full"></div>
                </div>
              </div>
              
              <div className="lg:w-3/4 text-center lg:text-left">
                <h4 className="text-3xl font-bold text-card-foreground mb-3">
                  {bonusModule.module} <span className="text-secondary">(exploring)</span>
                </h4>
                <p className="text-xl text-muted-foreground leading-relaxed mb-6">
                  {bonusModule.title}
                </p>
                <div className="grid md:grid-cols-2 gap-4">
                  {bonusModule.benefits.map((benefit, benefitIndex) => (
                    <div key={benefitIndex} className="flex items-start bg-background/30 rounded-xl p-4">
                      <span className="text-secondary mr-3 text-xl font-bold">→</span>
                      <p className="text-muted-foreground">{benefit}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ComingSoonSection;