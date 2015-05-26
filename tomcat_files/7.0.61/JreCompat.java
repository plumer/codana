/*
 *  Licensed to the Apache Software Foundation (ASF) under one or more
 *  contributor license agreements.  See the NOTICE file distributed with
 *  this work for additional information regarding copyright ownership.
 *  The ASF licenses this file to You under the Apache License, Version 2.0
 *  (the "License"); you may not use this file except in compliance with
 *  the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package org.apache.tomcat.util.compat;

import java.util.Locale;

import javax.net.ssl.SSLEngine;
import javax.net.ssl.SSLServerSocket;

import org.apache.tomcat.util.res.StringManager;

/**
 * This is the base implementation class for JRE compatibility and provides an
 * implementation based on Java 6. Sub-classes may extend this class and provide
 * alternative implementations for later JRE versions
 */
public class JreCompat {

    private static final JreCompat instance;
    private static StringManager sm =
            StringManager.getManager(JreCompat.class.getPackage().getName());
    private static final boolean jre8Available;
    
    
    static {
        // This is Tomcat 7 with a minimum Java version of Java 6. The latest
        // Java version the optional features require is Java 8.
        // Look for the highest supported JVM first
        if (Jre8Compat.isSupported()) {
            instance = new Jre8Compat();
            jre8Available = true;
        } else if (Jre7Compat.isSupported()) {
            instance = new Jre7Compat();
            jre8Available = false;
        } else {
            instance = new JreCompat();
            jre8Available = false;
        }
    }
    
    
    public static JreCompat getInstance() {
        return instance;
    }
    
    
    // Java 7 methods
    
    public Locale forLanguageTag(String languageTag) {
        // Extract the language and country for this entry
        String language = null;
        String country = null;
        String variant = null;
        int dash = languageTag.indexOf('-');
        if (dash < 0) {
            language = languageTag;
            country = "";
            variant = "";
        } else {
            language = languageTag.substring(0, dash);
            country = languageTag.substring(dash + 1);
            int vDash = country.indexOf('-');
            if (vDash > 0) {
                String cTemp = country.substring(0, vDash);
                variant = country.substring(vDash + 1);
                country = cTemp;
            } else {
                variant = "";
            }
        }
        if (!isAlpha(language) || !isAlpha(country) || !isAlpha(variant)) {
            return null;
        }

        return new Locale(language, country, variant);
    }
    
    
    private static final boolean isAlpha(String value) {
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            if (!((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'))) {
                return false;
            }
        }
        return true;
    }
   
    
    // Java 8 methods
    
    public static boolean isJre8Available() {
        return jre8Available;
    }
    
    
    @SuppressWarnings("unused")
    public void setUseServerCipherSuitesOrder(SSLServerSocket socket,
            boolean useCipherSuitesOrder) {
        throw new UnsupportedOperationException(sm.getString("jreCompat.noServerCipherSuiteOrder"));
    }
    
    
    @SuppressWarnings("unused")
    public void setUseServerCipherSuitesOrder(SSLEngine engine,
            boolean useCipherSuitesOrder) {
        throw new UnsupportedOperationException(sm.getString("jreCompat.noServerCipherSuiteOrder"));
    }

}
