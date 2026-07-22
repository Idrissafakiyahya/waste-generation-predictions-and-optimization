import './About.css';

export default function About() {
  return (
    <div className="about-page">
      <section className="about-hero">
        <h1>About This System</h1>
        <p>Understanding Our Community Waste Reporting Initiative</p>
      </section>

      <div className="about-container">
        {/* Purpose Section */}
        <section className="about-section">
          <h2>Our Mission</h2>
          <p>
            The Community Waste Reporting System is designed to empower citizens 
            to contribute to a cleaner, healthier community. By making it easy to 
            report waste issues, we create a collaborative approach to waste 
            management that benefits everyone.
          </p>
          <p>
            Your reports help municipal authorities identify problem areas, 
            prioritize resources, and implement targeted solutions for 
            waste management.
          </p>
        </section>

        {/* Laws & Regulations */}
        <section className="about-section legal">
          <h2>Laws & Regulations</h2>
          <div className="regulations-content">
            <h3>Environmental Protection Standards</h3>
            <ul className="regulations-list">
              <li>
                <strong>Waste Management Act:</strong> All waste must be 
                properly managed according to national and local regulations.
              </li>
              <li>
                <strong>Environmental Health Standards:</strong> Community waste 
                must not pose health or safety risks to residents.
              </li>
              <li>
                <strong>Public Health Ordinance:</strong> Proper waste containment 
                and disposal is mandatory for all community areas.
              </li>
              <li>
                <strong>Local Municipality Guidelines:</strong> Each Shehia 
                follows specific waste collection and management protocols.
              </li>
            </ul>

            <h3>Reporting Requirements</h3>
            <ul className="regulations-list">
              <li>
                Reports must include accurate location information (Shehia and 
                specific bin location)
              </li>
              <li>
                Timestamps should reflect when the issue was observed
              </li>
              <li>
                Comments should be factual and constructive
              </li>
              <li>
                False or malicious reports may result in account restrictions
              </li>
            </ul>

            <h3>Community Responsibilities</h3>
            <ul className="regulations-list">
              <li>
                Report only persistent or serious waste management issues
              </li>
              <li>
                Provide accurate information to aid city staff response
              </li>
              <li>
                Respect municipal collection schedules
              </li>
              <li>
                Participate constructively in waste solutions
              </li>
            </ul>
          </div>
        </section>

        {/* Privacy & Data Protection */}
        <section className="about-section privacy">
          <h2>Privacy & Data Protection</h2>
          
          <h3>Data Collection</h3>
          <p>
            When you submit a waste report, we collect the following information:
          </p>
          <ul className="privacy-list">
            <li>Location (Shehia and bin identifier)</li>
            <li>Timestamp of the report submission</li>
            <li>Comments you provide</li>
            <li>Optional: Your contact information for follow-ups</li>
          </ul>

          <h3>How We Use Your Data</h3>
          <p>
            Your data is used to:
          </p>
          <ul className="privacy-list">
            <li>Identify waste management issues and trends</li>
            <li>Inform municipal planning and resource allocation</li>
            <li>Improve waste collection schedules and efficiency</li>
            <li>Respond to community concerns promptly</li>
            <li>Generate reports for city administration</li>
          </ul>

          <h3>Data Security</h3>
          <p>
            We take data security seriously:
          </p>
          <ul className="privacy-list">
            <li>All data is encrypted during transmission (HTTPS)</li>
            <li>Access is restricted to authorized municipal staff only</li>
            <li>Data is stored securely on protected servers</li>
            <li>Regular security audits are conducted</li>
            <li>We comply with all local data protection regulations</li>
          </ul>

          <h3>Anonymity & Privacy Rights</h3>
          <p>
            You have the right to submit reports anonymously. However:
          </p>
          <ul className="privacy-list">
            <li>
              Anonymous reports help with data analysis and trend identification
            </li>
            <li>
              Follow-up communication may not be possible for anonymous reports
            </li>
            <li>
              Your personal information will never be shared with third parties 
              without consent
            </li>
            <li>
              You may request deletion of your data (subject to legal requirements)
            </li>
          </ul>

          <h3>Data Retention</h3>
          <p>
            Reports are retained for 2 years for administrative and statistical 
            purposes. After this period, identifiable information is removed while 
            aggregate data is retained for long-term planning.
          </p>

          <h3>Contact & Rights</h3>
          <p>
            If you have questions about your data or wish to exercise your privacy 
            rights, contact:
          </p>
          <p className="contact-info">
            <strong>Waste Prediction Group</strong><br />
            Email: wastepredictiongroup2@gmail.com<br />
            Phone: 622923299
          </p>
        </section>

        {/* Support Section */}
        <section className="about-section support">
          <h2>Support & Questions</h2>
          <p>
            For more information about this system or if you have questions about 
            waste management in your area, please contact Waste Prediction Group.
          </p>
          <div className="contact-box">
            <p>
              <strong>Email:</strong> wastepredictiongroup2@gmail.com
            </p>
            <p>
              <strong>Phone:</strong> 622923299
            </p>
            <p>
              <strong>Hours:</strong> Monday - Friday, 8:00 AM - 5:00 PM
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
